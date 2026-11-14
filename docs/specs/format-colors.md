# format-colors — 站点配色规约（Catppuccin Latte / Mocha）

> 适用范围：根 `index.html`、`interview.html`、`core/`（章节站）、三个子站（`Software-Engineering-*` / `java-design-patterns-principles`）及其共享样式。
> **唯一色源（SSOT）**：`docs/catppuccin-tokens.json`。本文色表仅为速查，若与 JSON 冲突以 JSON 为准。
> 门禁：`python3 docs/scripts/scripts/audit_catppuccin.py`（交付前必须 ALL PASS，见 §7）。

## 1. 色彩体系

全站采用 **Catppuccin** 官方稳定版调色板，双风味：

- **浅色主题 = Latte**（唯一亮色风味：奶白底 + 饱和强调色）
- **暗黑主题 = Mocha**（最深暗色风味：深底 + 柔彩）

不引入第三风味，不引入 Tailwind / One-Dark 等旧色系的任何 hex（包括注释与示例里的写样）。

## 2. 主题壳结构（强制）

所有站点样式必须用「三块」结构，换肤只改 CSS 变量：

```css
:root {                 /* 浅色 = Latte */
  --accent: #1e66f5;    /* Latte blue */
}
html[data-theme="dark"] {          /* 显式暗黑 = Mocha */
  --accent: #89b4fa;
}
@media (prefers-color-scheme: dark) {   /* 自动暗黑兜底（跟随系统） */
  html:not([data-theme="light"]) {
    --accent: #89b4fa;
  }
}
```

- 新页必须在 CSS 之前加载 `core/assets/theme-init.js`（防闪白，红线 7）。
- 显式暗黑块与自动暗黑块必须同步改，两处值一致。
- 三子站共享令牌在 `docs/shared/style/satellite-base.css`，站内专属写各站 `assets/style.css`。

## 3. 官方全套色（速查表）

完整 26 色 × 2 风味以 `docs/catppuccin-tokens.json` 的 `flavors` 为准。速查：

| 语义 | Latte | Mocha |
|---|---|---|
| rosewater | `#dc8a78` | `#f5e0dc` |
| flamingo | `#dd9a9a` | `#f2cdcd` |
| pink | `#ea76cb` | `#f5c2e7` |
| mauve | `#8839ef` | `#cba6f7` |
| red | `#d20f39` | `#f38ba8` |
| maroon | `#e64553` | `#eba0ac` |
| peach | `#fe640b` | `#fab387` |
| yellow | `#df8e1d` | `#f9e2af` |
| green | `#40a02b` | `#a6e3a1` |
| teal | `#179299` | `#94e2d5` |
| sky | `#04a5e5` | `#89dceb` |
| sapphire | `#209fb5` | `#74c7ec` |
| blue | `#1e66f5` | `#89b4fa` |
| lavender | `#7287fd` | `#b4befe` |
| text | `#4c4f69` | `#cdd6f4` |
| subtext1 | `#5c5f77` | `#bac2de` |
| subtext0 | `#6c6f85` | `#a6adc8` |
| overlay2 | `#7c7f93` | `#9399b2` |
| overlay1 | `#8c8fa1` | `#7f849c` |
| overlay0 | `#9ca0b3` | `#6c7086` |
| surface2 | `#ccd0da` | `#585b70` |
| surface1 | `#bcc0cc` | `#45475a` |
| surface0 | `#dce0e8` | `#313244` |
| base | `#eff1f5` | `#1e1e2e` |
| mantle | `#e6e9ef` | `#181825` |
| crust | `#dce0e8` | `#11111b` |

## 4. 语义令牌映射（既有约定）

| 令牌/体系 | Latte（浅） | Mocha（暗） |
|---|---|---|
| `--accent` 强调 | blue `#1e66f5` | blue `#89b4fa` |
| `--accent-alt` 次强调 | mauve `#8839ef` | mauve `#cba6f7` |
| `--danger` 危险 | red `#d20f39` | red `#f38ba8` |
| `--dim` / `--svg-dim` | overlay2 `#7c7f93` | overlay2 `#9399b2` |
| `--muted` / `--svg-muted` | subtext0 `#6c6f85` | subtext0 `#a6adc8` |
| `--border-strong` | overlay0 `#9ca0b3` | surface2 `#585b70` |
| 难度：专家 / 架构师 / 高级 | teal `#179299` / mauve `#8839ef` / blue `#1e66f5` | teal / mauve / blue（Mocha 值） |
| 道法术器（Core 子站） | mauve / yellow / blue / teal | 同语义 Mocha 值 |
| 深度透镜 i1~i9（Core） | blue, mauve, green, yellow, pink, teal, peach, lavender, red（九色无重复） | 同语义 Mocha 值 |
| `.heat` 五级热力（由浅到深） | surface2 `#cdd6f4` → lavender `#b4befe` → lavender `#7287fd` → blue `#1e66f5` → blue 同相降明度 `#153a84` | 暗黑沿用（热力条为色阶语义，不随主题翻转） |

规则：**新增令牌先在此登记语义与两风味值，再写代码**；禁止同语义两种色相。

## 5. 图表（Mermaid / 内联 SVG）配色

1. **HTML/JS 源里的图表内联色一律写 Latte 值**（浅色画布为基准）。暗黑由 `theme-init.js` 运行时重着色：
   - `MERMAID_VARS_LIGHT` / `MERMAID_VARS_DARK`：Mermaid themeVariables 两套；
   - `RETINT_FILL_DARK` / `RETINT_STROKE_DARK`：内联 `fill:`/`stroke:` 的深色重着色映射（同色相降明度）。
2. **图表新增内联 fill/stroke 色，必须同步登记 `theme-init.js` 的 RETINT 两个 map**，否则暗黑下浅色块压暗字不可读（对比度 1.0）。门禁第 2 项强制校验：HTML 内联图表 hex 必须被 RETINT 键集覆盖。
3. `MERMAID_VARS_DARK` 的 `cScale*` 分支暗底、RETINT 目标值等「同色相降明度」派生值，全部登记于 JSON `derived.dark`。
4. 第三方图表库（`docs/shared/js/*.min.js`）不在规约范围，禁止手改其源码。

## 6. 派生色与豁免台账

- **派生色**（JSON `derived`）：官方 palette 之外、有明确用途的项目自定值，必须带 `key` + `reason`（如 Mermaid cScale 暗底、RETINT 目标、Core dark 渐变端点）。新增派生值必须先登记再用。
- **豁免**（JSON `exempt`）：允许出现的非 palette hex，目前仅两项——`#000000`（`@media print` 正文纯黑）与 `#ffffff`（打印底白 / 徽章配套白字语义 / SVG 文字 halo）。豁免是台账不是后门：**禁止**为绕过门禁把违规色塞进 exempt，新增豁免须写明不可替代的理由。

## 7. 门禁

```bash
python3 docs/scripts/audit_catppuccin.py
```

检查项：

1. **hex 全量扫描**：站点自有文件（排除 `tmp/`、`rk/`、`docs/facts/`、`node_modules/`、第三方 `*.min.js` 等，范围配置在 JSON `scan`）中，颜色上下文（CSS 声明值、HTML `style` 属性、SVG `fill=`/`stroke=` 属性、JS 字符串字面量与注释）出现的每个 hex，必须 ∈ palette ∪ derived ∪ exempt。HTML `href="#…"` 锚点不算颜色。
2. **RETINT 覆盖**：HTML 内联图表 `fill:`/`stroke:` colon 形 hex 必须被 `theme-init.js` 的 `RETINT_FILL_DARK` ∪ `RETINT_STROKE_DARK` 键集覆盖。

门禁配置（扫描范围、palette、派生、豁免）**全部数据化于 `docs/catppuccin-tokens.json`**，脚本内不写死任何色值、路径或文件清单；项目根定位统一走 `.workbuddy/skills/java-kb-expand/scripts/_kbroot.py::find_root`。

probe 双向验证（改门禁后必跑）：

```bash
python3 docs/scripts/probe_catppuccin_gate.py
```

用例：注入非 palette hex 到 CSS → 必 FAIL；注入未登记的内联图表 hex 到 HTML → 必 FAIL；还原后 → 必 PASS。注入使用 try/finally 还原，不依赖临时目录夹具。

## 8. 交付前自查清单（配色维度）

1. `python3 docs/scripts/audit_catppuccin.py` → ALL PASS；
2. 若改过门禁脚本或 JSON 结构 → 加跑 `python3 docs/scripts/probe_catppuccin_gate.py` → 双向 PASS；
3. 新增图表内联色 → 已同步登记 RETINT 与（如为派生值）JSON `derived`；
4. 注释与文档中的示例色也必须合规（门禁会扫注释里的 hex）。
