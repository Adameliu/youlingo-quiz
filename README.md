# Youlingo 友邻国 🎯

多语言沉浸式学习平台 —— 通过科学间隔重复 + 多样化题型，高效掌握词汇与语法。

## ✨ 功能特色

### 📚 多语言支持
- **德语**（A1–B2 全模块，24 个模块，含语法、阅读、小视频）
- **英语**（独立词库模块）
- 一键切换语言，进度独立保存

### 🧠 智能复习算法
- 基于间隔重复（Spaced Repetition）的渐进式复习算法
- 答对按 **1h → 2h → 5h → 25h → 4d → 10d → 20d → 40d** 递增间隔
- 答错 1 分钟后再现，巩固薄弱点
- "太简单了"一键标记已掌握
- "42天后"暂不复习

### 🎯 多样化题型
| 题型 | 说明 |
|---|---|
| 默写（Dictation） | 听音频拼写单词 |
| 中文默写 | 看中文写外语 |
| 词义选择 | 从选项中选择正确词义 |
| 选择题 | 四选一 / 多选 |
| 词性判断 | 判断名词阴阳中 |
| 复数形式 | 输入名词复数 |
| 动词变位 | 现在时 / 过去时变位 |
| 分词 | 第二分词 / 过去分词 |
| 可分前缀 | 判断可分动词 |
| 比较级 / 最高级 | 形容词比较级变化 |
| 短语 / 自定义 | 自由练习 |

### 🎮 学习模式
- **自由模式**：按模块 → 小节进入，自由练习
- **顺序模式**：点击"开始学习"，自动按顺序推进，完成一节自动进入下一节
- **多字段答题**：同时检查多个答案项（如冠词 + 名词）

### 🔐 用户系统
- **Firebase 邮箱登录**：进度云端同步，多设备无缝衔接
- **Demo 模式**：无需注册，本地体验全部功能

### 📱 PWA 支持
- 可安装到手机桌面，独立运行（无浏览器地址栏）
- 离线可加载已缓存资源
- 安装按钮一键安装

### 📊 学习统计
- 今日学习卡片数实时显示
- 待复习卡片数量一目了然
- 进度条直观展示学习完成度

## 🚀 在线体验

👉 [liuyu.at](https://liuyu.at)

## 🛠️ 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 原生 HTML + CSS + JavaScript（Vanilla JS） |
| 样式 | Bootstrap 5.3 + 自定义 CSS |
| 后端 | Firebase Realtime Database |
| 认证 | Firebase Authentication（邮箱登录） |
| 部署 | Vercel（自动从 GitHub 部署） |
| 域名 | Cloudflare DNS + CDN |
| 存储 | Cloudflare R2（音频文件） |
| 版本控制 | Git + GitHub |

## 📁 项目结构

```
├── study_app.html      # 主应用（单页应用）
├── index.html          # 同 study_app.html（Vercel 入口）
├── vercel.json         # Vercel 配置
├── .vercelignore       # Vercel 忽略文件
├── service-worker.js   # PWA 离线缓存
├── manifest.json       # PWA 清单
├── icon-192.png        # PWA 图标
├── icon-512.png        # PWA 大图标
├── study_data_compact.json  # 德语数据（压缩）
├── english_data.json   # 英语数据
└── .gitignore          # Git 忽略规则
```

## 🧪 本地运行

直接用浏览器打开 `study_app.html` 即可运行（需联网加载 Bootstrap 和 Firebase SDK）。

```bash
# 克隆仓库
git clone https://github.com/Adameliu/youlingo-quiz.git

# 直接用浏览器打开 study_app.html
# 或使用本地服务器
python -m http.server 8080
```

## 🔧 部署说明

推送至 GitHub 后，Vercel 自动部署：

1. Fork / 推送代码到 GitHub
2. 在 [Vercel](https://vercel.com) 导入该项目
3. 设置域名（可选）
4. 每次 `git push` 自动部署

> 需要自行配置 Firebase 项目和 Cloudflare R2 存储桶。

## 📌 注意事项

- 音频文件存储于 Cloudflare R2，需自建存储桶并更新 `R2_BASE` 变量
- Firebase 配置需替换为自己的 `firebaseConfig`
- Demo 模式下进度仅保存在浏览器本地
