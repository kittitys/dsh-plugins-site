# dsh-plugins-site

DSH 插件官网（多插件共用）。纯静态、零脚本、零外部依赖（不引用 CDN、字体、统计）。

线上地址：**https://plugins.zhangyongxi.cc**（Cloudflare Pages + 自定义域名）

## 目录约定

```
index.html                    # 插件列表（新插件在这里加一张卡）
dsh-mem0-memory/index.html    # 每个插件一个目录，页面地址 = 插件市场里填的官网地址
assets/site.css               # 全站唯一样式
CNAME                         # GitHub Pages 用（Cloudflare Pages 忽略）
.nojekyll                     # 防止 GitHub Pages 跑 Jekyll
```

新增一个插件 = 复制 `dsh-mem0-memory/` 改内容 + 在 `index.html` 加一张卡。不需要构建。

## 为什么要有这个站（别删）

插件市场上架时，如果填了「反链」（本站在同一域名下放一个指向插件市场的 dofollow 链接），
平台会几小时自动校验、约 24 小时自动发布；留空则走人工审核（几天）。

因此本站的规则：

1. **每个插件页必须保留指向插件市场的 dofollow 链接**（页面底部 footer）。
   - 写法：`<a href="https://cordis.run">…</a>`，**不要**加 `rel="nofollow"`。
2. 插件在市场上登记时，「官网/Website」一栏填的就是该插件页的完整 URL（同域名）。
3. 站点必须是公开可访问（不能有登录墙），否则校验失败退回人工。

## 部署（Cloudflare Pages，推荐）

一次配置，之后 `git push` 自动发布。

1. Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. 选择仓库 `kittitys/dsh-plugins-site`，分支 `master`
3. 构建配置：**Framework preset = None**，Build command 留空，Build output directory = `/`
4. 保存后进入项目 → **Custom domains** → 添加 `plugins.zhangyongxi.cc`
   （DNS 已在 Cloudflare，会自动创建 CNAME；HTTPS 证书自动签发）
5. 打开 `https://plugins.zhangyongxi.cc` 验证

> 备选：GitHub Pages。仓库设置 → Pages → Source 选 `master` / 根目录，
> 自定义域名填 `plugins.zhangyongxi.cc`（`CNAME` 文件已就位），再在 DNS 加 CNAME 指向 `kittitys.github.io`。

## 本地预览

```powershell
# 任意静态服务器即可，例如
python -m http.server 8791 --directory "D:\Users\kitti\.openclaw\workspace\projects\DSH practice\script\dsh-plugins-site"
```

## 维护

- 内容来源：插件的 README / CHANGELOG（版本号、兼容性表要与 npm 上的一致）
- 发新版后记得同步页面上的版本徽章与兼容性表
- 样式只有 `assets/site.css` 一个文件，改配色在 `:root` 变量里
