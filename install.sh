#!/usr/bin/env bash
set -euo pipefail

# ─── 土味情话 CLI 一键安装脚本 ───
# curl -sL https://raw.githubusercontent.com/lirixiang/mac-tools/master/install.sh | bash

REPO="https://github.com/lirixiang/mac-tools.git"
INSTALL_DIR="$HOME/.mac-tools"
BIN_NAME="qinghua"
BIN_LINK="$HOME/.local/bin/$BIN_NAME"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
MAGENTA='\033[0;35m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
err()   { echo -e "${RED}[✗]${NC} $1"; exit 1; }

echo -e "${MAGENTA}"
cat << 'BANNER'
 ╔══════════════════════════════════════╗
 ║   💕 土味情话 CLI 一键安装           ║
 ║   1000+ 条情话，随叫随到             ║
 ╚══════════════════════════════════════╝
BANNER
echo -e "${NC}"

# ─── 检查依赖 ───
command -v git  >/dev/null 2>&1 || err "需要 git，请先安装: brew install git"
command -v python3 >/dev/null 2>&1 || err "需要 python3，请先安装: brew install python"

# 检查 uv 或 pip
HAS_UV=false
if command -v uv >/dev/null 2>&1; then
    HAS_UV=true
    info "检测到 uv"
else
    warn "未检测到 uv，将使用 pip"
fi

# ─── 克隆/更新仓库 ───
if [ -d "$INSTALL_DIR" ]; then
    info "已存在 $INSTALL_DIR，拉取最新代码..."
    cd "$INSTALL_DIR" && git pull --ff-only origin master 2>/dev/null || true
else
    info "克隆仓库到 $INSTALL_DIR..."
    git clone --depth 1 "$REPO" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# ─── 创建虚拟环境并安装 ───
if [ "$HAS_UV" = true ]; then
    if [ ! -d ".venv" ]; then
        info "创建虚拟环境 (uv)..."
        uv venv --python python3 >/dev/null 2>&1
    fi
    info "安装依赖..."
    uv pip install -e . >/dev/null 2>&1
else
    if [ ! -d ".venv" ]; then
        info "创建虚拟环境 (venv)..."
        python3 -m venv .venv
    fi
    info "安装依赖..."
    .venv/bin/pip install -e . >/dev/null 2>&1
fi

# ─── 创建可执行链接 ───
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/.venv/bin/$BIN_NAME" "$BIN_LINK"
info "已创建命令: $BIN_LINK"

# ─── 配置 PATH 和 alias ───
SHELL_RC=""
if [ -n "${ZSH_VERSION:-}" ] || [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

if [ -n "$SHELL_RC" ]; then
    # 确保 ~/.local/bin 在 PATH 中
    if ! grep -q '.local/bin' "$SHELL_RC" 2>/dev/null; then
        echo '' >> "$SHELL_RC"
        echo '# mac-tools PATH' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        info "已添加 ~/.local/bin 到 PATH ($SHELL_RC)"
    fi

    # 添加情话 alias
    if ! grep -q 'alias 情话' "$SHELL_RC" 2>/dev/null; then
        echo '' >> "$SHELL_RC"
        echo '# 土味情话' >> "$SHELL_RC"
        echo 'alias 情话="qinghua --type=rand_nothings"' >> "$SHELL_RC"
        info "已添加 alias: 情话"
    fi

    # 开终端自动显示情话
    if ! grep -q 'rand_nothings' "$SHELL_RC" 2>/dev/null; then
        echo '' >> "$SHELL_RC"
        echo '# 开终端自动来一波土味情话' >> "$SHELL_RC"
        echo 'qinghua --type=rand_nothings 2>/dev/null' >> "$SHELL_RC"
        info "已配置开终端自动显示情话"
    fi
fi

# ─── 完成 ───
echo ''
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN} 安装完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ''
echo -e " 使用方法:"
echo -e "   ${MAGENTA}qinghua --type=rand_nothings${NC}   随机 20 条情话"
echo -e "   ${MAGENTA}qinghua --type=menu${NC}            查看 80 个分类"
echo -e "   ${MAGENTA}qinghua --type=talk --key=撩妹${NC} 按关键词搜话术"
echo -e "   ${MAGENTA}qinghua --type=nothings --key=月亮${NC} 搜土味情话"
echo -e "   ${MAGENTA}情话${NC}                           随机情话快捷方式"
echo ''
echo -e " 重启终端或执行 ${YELLOW}source $SHELL_RC${NC} 立即生效"
echo ''

# 来一条尝尝鲜
echo -e "${MAGENTA}── 先来一条尝尝鲜 ──${NC}"
"$INSTALL_DIR/.venv/bin/$BIN_NAME" --type=rand_nothings 2>/dev/null | head -1
echo ''
