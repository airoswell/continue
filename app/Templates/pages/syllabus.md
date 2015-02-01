# Build your personal website in 40-something minutes

## Tools (pre-requisite)
### 1. Sublime Text
- #### [Sublime Text website](http://www.sublimetext.com/)
- #### Recommend `Sublime Text 3 Beta`
- #### Basic usage
    - Normal text editor
    - `Tab` key to **auto complete** and **indent**
    - `Cmd` + `/` OR `Ctrl` + `/` to **comment**
    - `Cmd` + `d` or `Ctrl` + `d` to select subsequent identical strings
    - `Cmd` + `t` to jump to any file near by.

### 2. Google Chrome
- Open the **Developer Tool** by `Cmd` + `Option` + `J` on Mac, or `Ctrl` + `Shift` + `J` on Windows.


## Basic structures (quick summary, will encounter in actual example)
### 1. **Text data** and **links**
- `.html` files
- Made up of **Tags**: `<head>`, `<body>`, `<div>`, `<span>`, `<a>` and **Comments** `<!-- some comments -->`
    - ##### Closure
    - ##### Attributes:
        - Alphabetical characters and hyphen `-`
        - Values are surrounded by single quotes `''` or double quotes `""`
        - Most important basic attributes
            - `class`: `<div class='button button-small'></div>`
            - `style`: `<span style='font-size:20px;'></span>`
            - `id`: `<span id='introduction'></span>`
        - Allow arbitrary attributes for advanced usage
            - `layout`: `<div layout='row'></div>`
            - `layout-align`: `<div layout='row' layout-align='start center'></div>`
            - `flex`: `<div flex='50'></div>`
    - ##### Text content: Texts you want to display


### 2. **visual style**
- `.css` files
- Made up of **selectors** and **style settings**
### 3. **Dynamics** and **reaction to user's action**
- `.js` files
- We will not discuss detail, but will encounter some convenient 3rd party packages.


## Actual Example
### 1. Use `Sublime Text` to generate a back-bone `index.html` structure:
- Save a `index.html` file
- Type `doc` and hit `Tab` key
- Get to [https://github.com/angular/material#installing](https://github.com/angular/material#installing), copy the following code

        <!-- <head> -->
        <!-- Angulars Material CSS now available via Google CDN; version 0.7 used here -->
        <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/angular_material/0.7.0/angular-material.min.css">


        <!-- end of <body> -->
        <!-- Angular Material Dependencies -->
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-animate.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-aria.min.js"></script>


        <!-- Angular Material Javascript now available via Google CDN; version 0.7 used here -->
        <script src="//ajax.googleapis.com/ajax/libs/angular_material/0.7.0/angular-material.min.js"></script>

- **header** and **content** section, with comments
- **header** section
    - introduce `style` attributes
        - `font-size` and `color`
        - `background`
        - `border`
        - `padding` and `margin` (box-model)
    - Introduce `.css` file to store all styling, introduce `class`
- **header** `button` `class`
    - Introduce `layout` and `layout-align`
        - `layout`: `row` and `column`
        - `layout-align`: `start`, `end`, `center`
- **content**: **cover image**
    - `style="background: url(images/cover.jpg); background-size:100%"`
    - Use `layout` and `layout-align` to place **welcome** message in the middle
- **content**: **self-introduction**
    - Introduce the combination of `layout` and `flex` to center intro-section
    - Introduce generic attributes (`bd-black`, `bd-blue`) as `css selectors`.
    - Introduce **opacity** of `.gif` and `.png`
    - Emphasize generic `class` names for re-usability.
- **content**: **Publications**
    - Review `layout` and `layout-align`
    - Introduce `<a>` tag and add links
- **header**: add link to paper and create `paper.html`
- Use **Chrome** to fine tune styling.

### 2. Putting the pages on the web (byethost.com)