# 历史缺陷检查表

提炼自 2026 年三期 CANN ops-cv PR 的检视及 AdaptiveThreshold、FloodFill、LaplacianOfGaussian 的开发记录。下面是风险模式与反例思路，不是对这些算子当前状态的缺陷断言。历史评论可能已修复或被撤回；先核实当前实现和目标平台。

| 触发改动/风险 | 检查方法 | 最小回归方向 | 历史来源 |
| --- | --- | --- | --- |
| tile、halo、滑窗变化 | clamp 基于整图还是当前 tile；进入/离开列是否初始化 | 非整 tile 宽度、窄于窗口、跨 tile 边界、单行/单列 | AdaptiveThreshold #1528 |
| 2D 搬运/尾块 | 分配 pitch 与 src/dst stride 一致；确认所用重载的字节/元素/块单位 | 尾块宽不是对齐单位倍数，至少两行；检查基址与长度 | DistanceTransform #1537、IntegralImage #1539 |
| 分阶段/回退缓冲复用 | 每条访问路径最大索引都落在实际分配内，尾块回退也核算 | phase A/B 不同 tile 宽、通道边界、最后一行进入通用分支 | IntegralImage #1539、MatchTemplate #1872 |
| UB 预算与尺寸变化 | 队列深度、对齐、halo、临时量和分支缓冲全部计入；不能把预算算出 0 强行钳成 1 | 刚好可行/不可行、空图大窗口、超宽图 | PixelShuffle #1531、AdaptiveThreshold #1528 |
| GM workspace | 核实该调用 ABI 的系统段与用户段，Host 大小/偏移与 Kernel 一致 | 多核共享区初始化、读写边界、连续调用污染 | MatchTemplate #1872、LoG 开发记录 |
| 同步缩减与缓存循环 | 追踪 MTE2→V、V→MTE3、V→MTE2 等生产消费依赖及缓冲重用 | 多次循环、双缓冲轮转、尾块、多次运行 | HitOrMiss #1515、LoG 开发记录 |
| 多核/回退 | barrier 参与者一致，空任务核不会提前退出必需同步；fallback 的复杂度可接受且披露 | 自然 span 溢出、梳齿/孤岛、mask、多核暂停恢复 | FloodFill #1905 |
| 大 shape/属性计算 | 乘法在溢出前检查；收窄、字节偏移、DMA 字段各有范围保障 | r 的幂、batch×H×W、超长 stride 的边界 Host UT | PixelShuffle #1531、SSIM #1644、GuidedFilter #2435 |
| 类型转换/舍入 | ReinterpretCast 不等于数值转换；显式处理 clamp、舍入和中间精度 | uint16 的 32767/32768/65535；阈值半整数两侧；窄化前溢出 | GammaCorrection #1533、AdaptiveThreshold #1528 |
| 浮点抵消/计数 | 求和次序或取消补偿后重测近零；检查计数超出 FP32 精确整数范围 | 高动态范围、翻转/新 seed、大窗口、精确计数边界 | LoG #2431、GoodFeaturesToTrack #1995 |
| batch/shape 推导 | 输入之间 batch 关系完整校验；每张图独立统计；UNKNOWN_DIM 不参与普通算术 | batch 1/多张且内容不同、混合已知/未知维度、shape-only 推导 | GoodFeaturesToTrack #1995、FloodFill #1905、GuidedFilter #2435 |
| 非连续输入/输出 | kernel 线性访问前有与工程相符的连续化或拒绝策略 | 带 stride 视图、输出描述符，接口与实现一起核实 | HOGDescriptor #2250、LoG #2431 |
| golden/比较器 | 独立数学实现，NaN/Inf 明确分类；测试预期不能从生产结果抄来 | sigma=0 等特殊属性、NaN 对 NaN、正常有限输出 | GaussianFilter3D #2040 |
| 模式/类型遗漏 | 模板实例化是否实际覆盖所有声称支持的分支 | 非空 Gaussian、多 dtype、optional 关闭、多核路径 | AdaptiveThreshold #1528、IntegralImage #1539、FloodFill #1905 |
| 接口与工程资产 | 验证生成 ACLNN、打包、示例链接及当前 CI，不只查目录是否存在 | 安装新包后编译最小调用；对应头文件和导出符号 | HitOrMiss #1515、DistanceTransform #1537、LoG #2431 |
| 文档与交付范围 | 最新 diff、测试入口、性能表和 issue 动机一致；不提交跳过 CI 的占位实现 | 干净 checkout 可获得关键测试和 benchmark；最终范围检查 | FloodFill #1905、GaussianFilter3D #2040、LoG #2431 |
| 错误清理/无用资源 | 所有失败分支释放 tensor、event、stream、device/workspace；删除前确认缓冲无消费者 | 在初始化/调用失败处检查清理路径，核算 UB | SSIM #1644、HOGDescriptor #2250 |

## 三个值得保留的判定例子

**AdaptiveThreshold：** UINT8 大窗口的窗口和可以被 FP32 精确表示，但加上半窗口面积后仍可能在取整边界丢失半单位，翻转二值输出。检查整个计算链，不以“输入是整数且小于 2^24”证明后续浮点运算精确。反例应覆盖边界两侧和实际流式/环形路径。

**FloodFill：** 小图成功不能证明生产 span 容量耗尽后的 fallback 正确。需要自然触发容量上限，并验证完整图像、mask、不可达孤岛和多核协议。最坏回退延迟也属于应披露的能力边界。

**LoG：** 取消补偿累加曾使版本更快，但稳定性/大图用例失败。恢复正确性后再比较性能。后续评审还推动将关键 runtime 数值测试和 benchmark 纳入仓库，说明“本机曾通过”与“交付后可复核”是两件事。

## 防止审查误报

MedianFilter3D #2456 的一次 cval 范围校验意见在复核中撤回：检查只读了 validation 文件，遗漏 tiling 中已有的联合校验。每个缺陷判断都应沿实际入口和调用链核实。

同样，不将 `.AutoContiguous()`、`GetUserWorkspace()`、手写 op_api、某种 barrier 或成对配置文件设为不分平台/接口的硬性规则。应证明当前契约需要什么、实际路径提供了什么，以及剩余缺口。

历史 PR 定位方式为 `https://gitcode.com/cann/ops-cv/pull/<编号>`。原始资料在来源工作区的 `support_docs_Global/references/PR代码审查汇总.md`，不属于运行依赖；部分摘要被截断，需原始细节时核实公开原评论，不能补造缺失文字。
