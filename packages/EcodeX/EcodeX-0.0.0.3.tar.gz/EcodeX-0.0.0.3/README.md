# EcodeX - SpadaOS官方GUI库

## 文档更新时间：2023/08/31

EcodeX是SpadaOS官方GUI库，它是一个功能强大、易于使用的Python库，用于创建现代化的图形用户界面应用程序用于SpadaOS的强大工具。

EcodeX基于EcoX框架开发，因此具有跨平台性，可以在Windows、Linux和MacOS等操作系统上运行。它提供了丰富的GUI元素和工具，以帮助开发者快速构建具有优秀用户体验的图形用户界面。这些GUI元素包括按钮、文本框、列表框、进度条等，同时也支持自定义元素和布局。

除了提供基本的GUI元素和布局，EcodeX还具备多种高级功能，如事件处理、主题管理和国际化支持等。这些功能使得开发者可以轻松地创建和管理复杂的图形用户界面应用程序。

EcodeX的API设计简洁明了，易于使用。开发者可以通过简单的代码来创建和管理GUI应用程序，极大地提高了开发效率。此外，EcodeX还提供了丰富的文档和示例，以帮助用户快速上手并理解如何使用该库。

总之，如果你正在寻找一个可靠、易于使用的GUI库，并且需要在SpadaOS操作系统上开发应用程序，那么EcodeX是一个值得考虑的选择。

## 作者

SpadaOS及EcodeX作者皆为EcoSpace

感谢帮助及支持SpadaOS及EcodeX的朋友们~

1. 龙龙&nbsp;&nbsp;QQ：2473307779

2. 事阿远捏_&nbsp;&nbsp;QQ：1298306141

3. 这是昵称&nbsp;&nbsp;QQ：2728399052

4. zqh7_&nbsp;&nbsp;QQ：3241417410

5. MarianaUI&nbsp;&nbsp;QQ：2323369467

如果有任何问题，可以加入EcodeX开发交流群哟~（QQ：909931264）

## 安装方式

EcodeX可以从pip安装:

```bash
pip install EcodeX
```

## 参考文档

### 1. Window类

```python
class Window() -> None:
```

#### 1.1 创建主窗口

**在执行 Window() 时请按照以下参数填写

```python
def __init__(
    self,
    title: str, # 窗口标题 若参数 is_border 为 False,此参数可不填
    icon: str, # 窗口图标 若参数 is_border 为 False,此参数可不填
    is_fullscreen: bool, # 是否全屏
    width: int, # 宽度（单位：px）若参数 is_fullscreen 为 True,此参数可不填
    height: int, # 高度（单位：px）若参数 is_fullscreen 为 True,此参数可不填
    is_border: bool, # 窗口是否有边框（无边框后用户不能移动窗口）
    is_circle: int, # 是否在窗口的四角修为圆角 若参数 is_fullscreen 为 False,此参数可不填
    circle: int, # 圆角的半径（单位：px）若参数 is_circle 为 False,此参数可不填
    index: int # 参见 1.2 ，在 1.1 创建基础窗口中不需要填写
    ) -> None: ...
```

#### 1.2 创建子窗口

```python
def child( #创建子窗口
    self,
    title: str, # 窗口标题 若参数 is_border 为 False,此参数可不填
    icon: str, # 窗口图标 若参数 is_border 为 False,此参数可不填
    is_fullscreen: bool, # 是否全屏
    width: int, # 宽度（单位：px）若参数 is_fullscreen 为 True,此参数可不填
    height: int, # 高度（单位：px）若参数 is_fullscreen 为 True,此参数可不填
    is_border: bool, # 窗口是否有边框（无边框后用户不能移动窗口）
    is_circle: int, # 是否在窗口的四角修为圆角 若参数 is_fullscreen 为 False,此参数可不填
    circle: int, # 圆角的半径（单位：px）若参数 is_circle 为 False,此参数可不填
    index: int # 子窗口的级别，级别越高显示越在上方
) -> Window: ...
```

#### 1.3 获取自己在窗口的信息

```python
def get( # 获取当前窗口信息
    self,
    type: str, # 可获取所有在 1.1 __init__ 参数的所有项，仅需要输入参数名称就行
) -> dict: ...
```

#### 1.4 更改自己窗口的信息

```python
def set(
    self,
    type: str, # 可更改所有在 1.1 __init__ 参数的所有项，仅需要输入参数名称就行
    to: str/bool/int # 要在参数 type 中更改的数
) -> None: ...
```

#### 1.5 添加 Element

若对 Element 类不熟悉的，请看2.1

```python
def append(
    self,
    element: Element # 要添加的 Element
) -> None: ...
```

#### 1.6 删除 Element

```python
def delete(
    self,
    element: Element # 要去除的 Element
) -> None: ...
```

### 2. Element类

```python
class Element() -> None: ...
```

#### 2.1 介绍

Element 类为 EcodeX 中自主创建的类型，可以在主/子窗口中添加文本/按钮等功能（就像html一样）
并且 Element 类的使用方法与 JavaScript 一致（除了innerHtml/innerText）

#### 2.2 Element 拥有的类型

可参考 ["这里"](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element) 的所有代码

#### 2.3 创建 Element 类

```python
def createElement(
    self,
    name: str # 要创建的 Element 类型
)
```

### 3.Install类
```python
class Install() -> None: ...
```

#### 2.1 初始化

```python
def pack(
    self,
    name, #软件名
    icon, #软件图标
    bao, #软件名名
    version, #软件版本
    version2, #软件更新次数
    install_requires, #所需的Python库及版本
    author, #软件作者
    author_email, #软件作者邮箱
    description #软件介绍
)
```

##### 软件名要求

1. 软件名称不得低于2个字

2. 软件名称中不得出现不宜词语

2. 软件名称中不得含有除主体程序外其他词汇（如：淘宝 - 双11特别版×&nbsp;&nbsp;&nbsp;&nbsp;淘宝√）

##### 软件图标要求

1. 软件图标背景不得为透明

2. 软件图标不应在四个角中出现内容（即软件图标在SpadaOS显示中为圆角）

3. 软件图标需与软件显示图标相同

4. 软件图表中不得有不宜图片

##### 软件包名要求

1. 格式要求：xxx.xxx.xxx

2. 上传版本时，包名应与旧版相同，否则请联系ecospace@qq.com

3. 包名中，不应未出现与软件相关的词汇（即淘宝：haha.baoming.hehe ×&nbsp;&nbsp;&nbsp;&nbsp;haha.baoming.taobao √）

4. 包名中不得出现不宜词语

##### 软件版本要求

1. 软件版本需比旧版版本号大

2. 软件版本应仅出现数字，不得出现其他字符

3. 软件版本格式要求：数字.数字.数字 / 数字.数字.数字.数字

##### 软件更新次数要求

1. 软件更新次数即软件第几次版本

2. 软件更新次数应仅比上一个版本大1（第一个版本除外）

3. 首次发布软件软件更新次数填写1，以后累加

##### 软件所需的Python库及版本要求

1. 若python库无要求，请留一个空列表[]

2. 若版本无要求，请留空

3. 格式要求
```python
[
    '这个库我要！':'版本是这个',
    '这个库我要！':'版本是这个',
    '这个库我要！':'版本是这个',
]
```

##### 软件作者要求

1. 若是公司，请填写全名

2. 若是个人，请填写真名或其他（要求：可以是主播名称，xx软件【xx软件不代表填写软件名！即若淘宝为李小明开发并发布的，名称可写“李小明软件”等】）

3. 若是外国人，名字为英文，请如实填写

4. 软件作者不得出现不宜词语

##### 软件邮箱要求

1. 该邮箱将作为以后软件更新使用

2. 邮箱不可为空箱（或临时生成邮箱等）

##### 软件介绍要求

1. 软件介绍必须围绕软件真实填写

2. 软件介绍不得出现不宜词语

3. 字数不得低于20字