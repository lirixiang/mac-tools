# 💕 土味情话 CLI

1000+ 条土味情话，随叫随到。支持分类查询、关键词搜索、随机抽取。

## 一键安装

```bash
curl -sL https://raw.githubusercontent.com/lirixiang/mac-tools/master/install.sh | bash
```

需要 `git` 和 `python3`，脚本会自动处理虚拟环境和 PATH 配置。

## 使用方法

```bash
# 随机 20 条情话
qinghua --type=rand_nothings

# 查看 80 个分类
qinghua --type=menu

# 按关键词搜话术
qinghua --type=talk --key=撩妹

# 搜土味情话
qinghua --type=nothings --key=月亮

# 快捷方式
情话
```

## 手动安装

```bash
git clone https://github.com/lirixiang/mac-tools.git ~/.mac-tools
cd ~/.mac-tools
python3 -m venv .venv
.venv/bin/pip install -e .

# 添加到 PATH
export PATH="$HOME/.mac-tools/.venv/bin:$PATH"
```

## 数据

- `SweetNothings.db` — SQLite 数据库，包含 `nothings`（情话）和 `talk_art`（话术）两张表
- `resources/` — 原始数据备份（SQL、JSON）
