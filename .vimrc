set nocompatible              " be iMproved, required
filetype off                  " required
 
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
 
" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" 代码自动缩进插件
Plugin 'vim-scripts/indentpython.vim'
" 代码补全插件
Plugin 'maralla/completor.vim'
" 语法检查插件
Plugin 'vim-syntastic/syntastic'
Plugin 'nvie/vim-flake8'
" 树形目录
Plugin 'scrooloose/nerdtree'
map <C-n> :NERDTreeToggle<CR>
" 树形目录添加git支持
Plugin 'Xuyuanp/nerdtree-git-plugin'
" tab键
Plugin 'jistr/vim-nerdtree-tabs'

" 美化状态栏
Plugin 'Lokaltog/vim-powerline'

" 缩进指示线
Plugin 'Yggdroot/indentLine'

" 代码格式化
Plugin 'tell-k/vim-autopep8'
autocmd FileType python noremap <buffer> <F8> :call Autopep8()<CR>
" 括号引号不全
Plugin 'jiangmiao/auto-pairs'
" 搜索插件 ctrl+p
Plugin 'kien/ctrlp.vim'
Plugin 'rking/ag.vim'


" git集成
Plugin 'tpope/vim-fugitive'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required



set nocompatible "关闭与vi的兼容模式
set number "显示行号
set nowrap    "不自动折行
set showmatch    "显示匹配的括号
set scrolloff=3        "距离顶部和底部3行"
set encoding=utf-8  "编码
set fenc=utf-8      "编码
set mouse=a        "启用鼠标
set hlsearch        "搜索高亮
syntax on    "语法高亮


au BufNewFile,BufRead *.py
\ set tabstop=2   "tab宽度
\ set softtabstop=4
\ set shiftwidth=4
\ set textwidth=79  "行最大宽度
\ set expandtab       "tab替换为空格键
\ set autoindent      "自动缩进
\ set fileformat=unix   "保存文件格式


" 分割窗口在右方或下方

set splitbelow
set splitright

" 窗口移动快捷键
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" 代码折叠 及快捷键
set foldmethod=indent
set foldlevel=99
nnoremap <space> za 


" 一键执行py文件 F5
map <F5> :call RunPython()<CR>
func! RunPython()
    exec "W"
    if &filetype == 'python'
        exec "!time python2.7 %"
    endif
endfunc



let NERDTreeIgnore=['\~$', '\.pyc$', '\.swp$']
