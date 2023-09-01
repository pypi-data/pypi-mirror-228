(self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || []).push([["lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0"],{

/***/ "./lib/components/filebrowser/FileBrowser.js":
/*!***************************************************!*\
  !*** ./lib/components/filebrowser/FileBrowser.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileBrowser": () => (/* binding */ FileBrowser),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/TreeView/TreeView.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/octicons-react */ "../../../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _jupyter_JupyterContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../../jupyter/JupyterContext */ "./lib/jupyter/JupyterContext.js");
/* harmony import */ var _jupyter_services_Services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../jupyter/services/Services */ "./lib/jupyter/services/Services.js");






const initialTree = {
    id: 'root',
    name: 'File Browser',
};
const FileBrowser = () => {
    const [tree, setTree] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(initialTree);
    const [, forceUpdate] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useReducer)(x => x + 1, 0);
    const { serviceManager } = (0,_jupyter_JupyterContext__WEBPACK_IMPORTED_MODULE_2__.useJupyter)();
    const loadPath = (services, subTree, path) => {
        const loadFolderItems = (services, path) => {
            const folderItems = services
                .contents()
                .get(path.join('/'))
                .then(res => {
                const items = res.content.map((e) => {
                    if (e.type === 'directory') {
                        return {
                            id: 'folder_' + e.name,
                            name: e.name,
                            children: new Array(),
                        };
                    }
                    else {
                        return {
                            id: 'file_' + e.name,
                            name: e.name,
                        };
                    }
                });
                const renderTree = items;
                renderTree.sort((a, b) => {
                    if ((a.id.startsWith("folder_")) && (b.id.startsWith("file_"))) {
                        return -1;
                    }
                    if ((a.id.startsWith("file_")) && (b.id.startsWith("folder_"))) {
                        return 1;
                    }
                    return a.name.localeCompare(b.name);
                });
                return renderTree;
            });
            return folderItems;
        };
        loadFolderItems(services, path).then(folderItems => {
            subTree.children = folderItems;
            for (const child of subTree.children) {
                if (child.id.startsWith('folder_')) {
                    loadPath(services, child, path.concat(child.name));
                }
            }
            setTree(initialTree);
            forceUpdate();
        });
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        if (serviceManager) {
            const services = new _jupyter_services_Services__WEBPACK_IMPORTED_MODULE_3__["default"](serviceManager);
            loadPath(services, initialTree, []);
        }
    }, [serviceManager]);
    const renderTree = (nodes) => {
        return nodes.map((node) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.Item, { id: node.id, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.LeadingVisual, { children: Array.isArray(node.children) ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.DirectoryIcon, {})) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_5__.FileIcon, {})) }), node.name, Array.isArray(node.children) && ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.SubTree, { children: renderTree(node.children) }))] })));
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.Item, { id: tree.id, defaultExpanded: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.DirectoryIcon, {}) }), tree.name, Array.isArray(tree.children) && ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__.TreeView.SubTree, { children: renderTree(tree.children) }))] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FileBrowser);


/***/ }),

/***/ "./lib/components/notebook/cell/prompt/Countdown.js":
/*!**********************************************************!*\
  !*** ./lib/components/notebook/cell/prompt/Countdown.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Countdown": () => (/* binding */ Countdown)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const Countdown = (props) => {
    const [count, setCount] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(props.count);
    let intervalRef = (0,react__WEBPACK_IMPORTED_MODULE_1__.useRef)();
    const decreaseNum = () => setCount((prev) => prev - 1);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setCount(props.count);
    }, [props.count]);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        intervalRef.current = setInterval(decreaseNum, 1000);
        return () => clearInterval(intervalRef.current);
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: ["[", count, "]"] }));
};


/***/ }),

/***/ "./lib/components/notebook/cell/prompt/CountdownInputPrompt.js":
/*!*********************************************************************!*\
  !*** ./lib/components/notebook/cell/prompt/CountdownInputPrompt.js ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CountdownInputPrompt": () => (/* binding */ CountdownInputPrompt),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Countdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Countdown */ "./lib/components/notebook/cell/prompt/Countdown.js");



const INPUT_PROMPT_CLASS = 'jp-InputPrompt';
class CountdownInputPrompt extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _executionCount = null;
    state = {
        count: 100
    };
    constructor() {
        super();
        this.addClass(INPUT_PROMPT_CLASS);
    }
    /** @override */
    render() {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_Countdown__WEBPACK_IMPORTED_MODULE_2__.Countdown, { count: this.state.count });
    }
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.state = {
                count: 0
            };
        }
        else {
            if (value === '*') {
                this.state = {
                    count: 0
                };
            }
            else {
                this.state = {
                    count: Number(value)
                };
                this.update();
            }
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CountdownInputPrompt);


/***/ }),

/***/ "./lib/components/output/OutputIPyWidgets.js":
/*!***************************************************!*\
  !*** ./lib/components/output/OutputIPyWidgets.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputIPyWidgets": () => (/* binding */ OutputIPyWidgets),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyter_lumino_IPyWidgetsAttached__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../jupyter/lumino/IPyWidgetsAttached */ "./lib/jupyter/lumino/IPyWidgetsAttached.js");



const OutputIPyWidgets = (props) => {
    const { view, state } = props;
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_jupyter_lumino_IPyWidgetsAttached__WEBPACK_IMPORTED_MODULE_1__["default"], { view: view, state: state }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (OutputIPyWidgets);


/***/ }),

/***/ "./lib/jupyter/Jupyter.js":
/*!********************************!*\
  !*** ./lib/jupyter/Jupyter.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Jupyter": () => (/* binding */ Jupyter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/ThemeProvider.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/BaseStyles.js");
/* harmony import */ var react_error_boundary__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-error-boundary */ "webpack/sharing/consume/default/react-error-boundary/react-error-boundary");
/* harmony import */ var react_error_boundary__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_error_boundary__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _JupyterContext__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./JupyterContext */ "./lib/jupyter/JupyterContext.js");
/* harmony import */ var _JupyterConfig__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./JupyterConfig */ "./lib/jupyter/JupyterConfig.js");
/* harmony import */ var _state_redux_Store__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../state/redux/Store */ "./lib/state/redux/Store.js");







/**
 * The component to be used as fallback in case of error.
 */
const ErrorFallback = ({ error, resetErrorBoundary }) => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("div", { role: "alert", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("p", { children: "Oops, something went wrong." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("pre", { children: error.message }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { style: { visibility: "hidden" }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("button", { onClick: resetErrorBoundary, children: "Try again" }) })] }));
};
/**
 * The Jupyter context. This handles the needed initialization
 * and ensure the Redux and the Material UI theme providers
 * are available.
 */
const Jupyter = (props) => {
    const { lite, startDefaultKernel, defaultKernelName, injectableStore, useRunningKernelId, useRunningKernelIndex, children, disableCssLoading, } = props;
    const config = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => (0,_JupyterConfig__WEBPACK_IMPORTED_MODULE_3__.loadJupyterConfig)(props), []);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        if (!config.insideJupyterLab) {
            if (!disableCssLoading) {
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_css_widgets-base_css"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_getUrl_js-node_modules_lumino_widgets_style_index_css"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_css_index_css-node_modules_jupyterlab_apputils_styl-92be6d"), __webpack_require__.e("lib_jupyter_lab_JupyterLabCss_js")]).then(__webpack_require__.bind(__webpack_require__, /*! ./lab/JupyterLabCss */ "./lib/jupyter/lab/JupyterLabCss.js"));
            }
        }
    }, [config]);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_error_boundary__WEBPACK_IMPORTED_MODULE_2__.ErrorBoundary, { FallbackComponent: ErrorFallback, onReset: () => { console.log('Error Boundary reset has been invoked...'); }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { colorMode: "day", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_JupyterContext__WEBPACK_IMPORTED_MODULE_6__.JupyterContextProvider, { baseUrl: (0,_JupyterConfig__WEBPACK_IMPORTED_MODULE_3__.getJupyterServerHttpUrl)(), defaultKernelName: defaultKernelName, disableCssLoading: disableCssLoading, injectableStore: injectableStore || _state_redux_Store__WEBPACK_IMPORTED_MODULE_7__["default"], lite: lite, startDefaultKernel: startDefaultKernel, useRunningKernelId: useRunningKernelId, useRunningKernelIndex: useRunningKernelIndex ?? -1, variant: "default", wsUrl: (0,_JupyterConfig__WEBPACK_IMPORTED_MODULE_3__.getJupyterServerWsUrl)(), children: children }) }) }) }));
};
Jupyter.defaultProps = {
    collaborative: false,
    defaultKernelName: 'python',
    disableCssLoading: false,
    lite: false,
    startDefaultKernel: true,
    terminals: false,
    useRunningKernelIndex: -1,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Jupyter);


/***/ }),

/***/ "./lib/jupyter/JupyterAuthError.js":
/*!*****************************************!*\
  !*** ./lib/jupyter/JupyterAuthError.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/**
 * Error class in case of Authentication or
 * Authorization exception.
 */
class JupyterAuthError extends Error {
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JupyterAuthError);


/***/ }),

/***/ "./lib/jupyter/JupyterConfig.js":
/*!**************************************!*\
  !*** ./lib/jupyter/JupyterConfig.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getJupyterServerHttpUrl": () => (/* binding */ getJupyterServerHttpUrl),
/* harmony export */   "getJupyterServerWsUrl": () => (/* binding */ getJupyterServerWsUrl),
/* harmony export */   "getJupyterToken": () => (/* binding */ getJupyterToken),
/* harmony export */   "loadJupyterConfig": () => (/* binding */ loadJupyterConfig),
/* harmony export */   "runsInJupyterLab": () => (/* binding */ runsInJupyterLab),
/* harmony export */   "setJupyterServerHttpUrl": () => (/* binding */ setJupyterServerHttpUrl),
/* harmony export */   "setJupyterServerWsUrl": () => (/* binding */ setJupyterServerWsUrl),
/* harmony export */   "setJupyterToken": () => (/* binding */ setJupyterToken)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The default Jupyter configuration.
 */
let config = {
    jupyterServerHttpUrl: '',
    jupyterServerWsUrl: '',
    jupyterToken: '',
    insideJupyterLab: false,
    insideJupyterHub: false,
};
/**
 * Setter for jupyterServerHttpUrl.
 */
const setJupyterServerHttpUrl = (jupyterServerHttpUrl) => {
    config.jupyterServerHttpUrl = jupyterServerHttpUrl;
};
/**
 * Getter for jupyterServerHttpUrl.
 */
const getJupyterServerHttpUrl = () => config.jupyterServerHttpUrl;
/**
 * Setter for jupyterServerWsUrl.
 */
const setJupyterServerWsUrl = (jupyterServerWsUrl) => {
    config.jupyterServerWsUrl = jupyterServerWsUrl;
};
/**
 * Getter for jupyterServerWsUrl.
 */
const getJupyterServerWsUrl = () => config.jupyterServerWsUrl;
/**
 * Setter for jupyterToken.
 */
const setJupyterToken = (jupyterToken) => {
    config.jupyterToken = jupyterToken;
};
/**
 * Getter for jupyterToken.
 */
const getJupyterToken = () => config.jupyterToken;
/**
 * Method to load the Jupyter configuration from the
 * host HTML page.
 */
const loadJupyterConfig = (props) => {
    const { lite, jupyterServerHttpUrl, jupyterServerWsUrl, collaborative, terminals, jupyterToken } = props;
    const jupyterHtmlConfig = document.getElementById('jupyter-config-data');
    if (jupyterHtmlConfig) {
        const jupyterConfig = JSON.parse(jupyterHtmlConfig.textContent || '');
        setJupyterServerHttpUrl(location.protocol + '//' + location.host + jupyterConfig.baseUrl);
        setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host + jupyterConfig.baseUrl);
        setJupyterToken(jupyterConfig.token);
        config.insideJupyterLab = jupyterConfig.appName === 'JupyterLab';
    }
    else {
        const datalayerHtmlConfig = document.getElementById('datalayer-config-data');
        if (datalayerHtmlConfig) {
            config = JSON.parse(datalayerHtmlConfig.textContent || '');
        }
        if (lite) {
            setJupyterServerHttpUrl(location.protocol + '//' + location.host);
        }
        else if (config.jupyterServerHttpUrl) {
            setJupyterServerHttpUrl(config.jupyterServerHttpUrl);
        }
        else {
            setJupyterServerHttpUrl(jupyterServerHttpUrl || location.protocol + '//' + location.host + "/api/jupyter");
        }
        if (lite) {
            setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host);
        }
        else if (config.jupyterServerWsUrl) {
            setJupyterServerWsUrl(config.jupyterServerWsUrl);
        }
        else {
            setJupyterServerWsUrl(jupyterServerWsUrl || location.protocol.replace('http', 'ws') + '//' + location.host + "/api/jupyter");
        }
        if (config.jupyterToken) {
            setJupyterToken(config.jupyterToken);
        }
        else {
            setJupyterToken(jupyterToken || '');
        }
    }
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('baseUrl', getJupyterServerHttpUrl());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('wsUrl', getJupyterServerWsUrl());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('token', getJupyterToken());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('collaborative', String(collaborative || false));
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('terminalsAvailable', String(terminals || false));
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('mathjaxUrl', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js');
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('mathjaxConfig', 'TeX-AMS_CHTML-full,Safe');
    /*
    PageConfig.getOption('hubHost')
    PageConfig.getOption('hubPrefix')
    PageConfig.getOption('hubUser')
    PageConfig.getOption('hubServerName')
    */
    config.insideJupyterHub = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('hubHost') !== "";
    return config;
};
const runsInJupyterLab = () => {
    const jupyterHtmlConfig = document.getElementById('jupyter-config-data');
    if (jupyterHtmlConfig) {
        const jupyterConfig = JSON.parse(jupyterHtmlConfig.textContent || '');
        return jupyterConfig.appName === 'JupyterLab';
    }
    return false;
};


/***/ }),

/***/ "./lib/jupyter/JupyterContext.js":
/*!***************************************!*\
  !*** ./lib/jupyter/JupyterContext.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterContext": () => (/* binding */ JupyterContext),
/* harmony export */   "JupyterContextConsumer": () => (/* binding */ JupyterContextConsumer),
/* harmony export */   "JupyterContextProvider": () => (/* binding */ JupyterContextProvider),
/* harmony export */   "createServerSettings": () => (/* binding */ createServerSettings),
/* harmony export */   "ensureJupyterAuth": () => (/* binding */ ensureJupyterAuth),
/* harmony export */   "useJupyter": () => (/* binding */ useJupyter)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_redux__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _JupyterConfig__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./JupyterConfig */ "./lib/jupyter/JupyterConfig.js");
/* harmony import */ var _JupyterHandlers__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./JupyterHandlers */ "./lib/jupyter/JupyterHandlers.js");
/* harmony import */ var _jupyter_lite_LiteServer__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../jupyter/lite/LiteServer */ "./lib/jupyter/lite/LiteServer.js");
/* harmony import */ var _services_kernel_Kernel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./services/kernel/Kernel */ "./lib/jupyter/services/kernel/Kernel.js");








/**
 * The instance for the Jupyter context.
 */
const JupyterContext = (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)(undefined);
const useJupyter = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(JupyterContext);
    if (!context)
        throw new Error("useContext must be inside a provider with a value.");
    return context;
};
/**
 * The type for the Jupyter context consumer.
 */
const JupyterContextConsumer = JupyterContext.Consumer;
/**
 * The type for the Jupyter context provider.
 */
const JupyterProvider = JupyterContext.Provider;
/**
 * Utiliy method to ensure the Jupyter context is authenticated
 * with the Jupyter server.
 */
const ensureJupyterAuth = (serverSettings) => {
    return (0,_JupyterHandlers__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(serverSettings, 'api', '').then(data => {
        return true;
    })
        .catch(reason => {
        console.log('The Jupyter Server API has failed with reason', reason);
        return false;
    });
};
/*
const headers = new Headers({
  "Cache-Control": "no-cache, no-store, must-revalidate",
  "Pragma": "no-cache",
  "Expires": "0",
});
*/
const createServerSettings = (baseUrl, wsUrl) => {
    return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings({
        baseUrl,
        wsUrl,
        appendToken: true,
        init: {
            mode: 'cors',
            credentials: 'include',
            cache: 'no-cache',
            //      headers,
        }
    });
};
/**
 * The Jupyter context provider.
 */
const JupyterContextProvider = (props) => {
    const { children, lite, startDefaultKernel, defaultKernelName, disableCssLoading, useRunningKernelId, useRunningKernelIndex, variant, baseUrl, wsUrl, injectableStore } = props;
    const [_, setVariant] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('default');
    const [serverSettings] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(createServerSettings(baseUrl, wsUrl));
    const [serviceManager, setServiceManager] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)();
    const [kernelManager, setKernelManager] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)();
    const [kernel, setKernel] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)();
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        if (lite) {
            (0,_jupyter_lite_LiteServer__WEBPACK_IMPORTED_MODULE_5__.startLiteServer)().then((serviceManager) => {
                setServiceManager(serviceManager);
                const kernelManager = serviceManager.sessions._kernelManager;
                setKernelManager(kernelManager);
                kernelManager.ready.then(() => {
                    console.log('Kernel Manager is ready', kernelManager);
                    if (startDefaultKernel) {
                        const kernel = new _services_kernel_Kernel__WEBPACK_IMPORTED_MODULE_6__["default"]({
                            kernelManager,
                            kernelName: defaultKernelName,
                            kernelType: "notebook",
                            kernelSpecName: "python",
                            serverSettings,
                        });
                        kernel.ready.then(() => {
                            console.log('Lite Kernel is ready', kernel.toString());
                            setKernel(kernel);
                        });
                    }
                });
            });
        }
        else {
            ensureJupyterAuth(serverSettings).then(isAuth => {
                if (!isAuth) {
                    const loginUrl = (0,_JupyterConfig__WEBPACK_IMPORTED_MODULE_7__.getJupyterServerHttpUrl)() + '/login?next=' + window.location;
                    console.warn('Redirecting to Jupyter Server login URL', loginUrl);
                    window.location.replace(loginUrl);
                }
                if (useRunningKernelId && useRunningKernelIndex > -1) {
                    throw new Error("You can not ask for useRunningKernelId and useRunningKernelIndex at the same time.");
                }
                if (startDefaultKernel && (useRunningKernelId || useRunningKernelIndex > -1)) {
                    throw new Error("You can not ask for startDefaultKernel and (useRunningKernelId or useRunningKernelIndex) at the same time.");
                }
                const serviceManager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServiceManager({ serverSettings });
                setServiceManager(serviceManager);
                const kernelManager = serviceManager.sessions._kernelManager;
                setKernelManager(kernelManager);
                kernelManager.ready.then(() => {
                    console.log('The Jupyter Kernel Manager is ready.');
                    /*
                    const running = kernelManager.running();
                    let kernel = running.next();
                    let i = 0;
                    while (! kernel.done) {
                      console.log(`This Jupyter server is hosting a kernel [${i}]`, kernel.value);
                      kernel = running.next();
                      i++;
                    }
                    */
                    if (useRunningKernelIndex > -1) {
                        const running = kernelManager.running();
                        let kernel = running.next();
                        let i = 0;
                        while (!kernel.done) {
                            if (i === useRunningKernelIndex) {
                                setKernel(new _services_kernel_Kernel__WEBPACK_IMPORTED_MODULE_6__["default"]({
                                    kernelManager,
                                    kernelName: defaultKernelName,
                                    kernelModel: kernel.value,
                                    kernelType: "notebook",
                                    kernelSpecName: "python",
                                    serverSettings,
                                }));
                                break;
                            }
                            kernel = running.next();
                            i++;
                        }
                    }
                    else if (startDefaultKernel) {
                        const defaultKernel = new _services_kernel_Kernel__WEBPACK_IMPORTED_MODULE_6__["default"]({
                            kernelManager,
                            kernelName: defaultKernelName,
                            kernelType: "notebook",
                            kernelSpecName: "python",
                            serverSettings,
                        });
                        defaultKernel.ready.then(() => {
                            setKernel(defaultKernel);
                        });
                    }
                });
            });
        }
        setVariant(variant);
    }, [lite, variant]);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_redux__WEBPACK_IMPORTED_MODULE_2__.Provider, { store: injectableStore, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(JupyterProvider, { value: {
                lite,
                serverSettings,
                serviceManager,
                kernelManager,
                defaultKernel: kernel,
                disableCssLoading,
                startDefaultKernel,
                variant,
                setVariant,
                baseUrl,
                wsUrl,
                injectableStore,
            }, children: children }) }));
};


/***/ }),

/***/ "./lib/jupyter/JupyterHandlers.js":
/*!****************************************!*\
  !*** ./lib/jupyter/JupyterHandlers.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _JupyterAuthError__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./JupyterAuthError */ "./lib/jupyter/JupyterAuthError.js");



/**
 * Call the Jupyter server API.
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(serverSettings, namespace = 'api', endPoint = '', init = {}) {
    // Make request to the Jupyter API.
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(serverSettings.baseUrl, namespace, endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, serverSettings);
        if (response.status === 403) {
            throw new _JupyterAuthError__WEBPACK_IMPORTED_MODULE_2__["default"]();
        }
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.warn('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/jupyter/ipywidgets/IPyWidgetsViewManager.js":
/*!*********************************************************!*\
  !*** ./lib/jupyter/ipywidgets/IPyWidgetsViewManager.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPyWidgetsViewManager": () => (/* binding */ IPyWidgetsViewManager),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_widgets_base_manager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base-manager */ "../../../../../node_modules/@jupyter-widgets/base-manager/lib/index.js");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base?5ccc");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyter-widgets/controls */ "webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls?27d1");
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_3__);




class IPyWidgetsViewManager extends _jupyter_widgets_base_manager__WEBPACK_IMPORTED_MODULE_1__.ManagerBase {
    el;
    constructor(el) {
        super();
        this.el = el;
    }
    async loadClass(className, moduleName, moduleVersion) {
        return new Promise(function (resolve, reject) {
            if (moduleName === '@jupyter-widgets/controls') {
                resolve(_jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_3__);
            }
            else if (moduleName === '@jupyter-widgets/base') {
                resolve(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__);
            }
            else {
                var fallback = function (err) {
                    let failedId = err.requireModules && err.requireModules[0];
                    if (failedId) {
                        console.log(`Falling back to jsDelivr for ${moduleName}@${moduleVersion}`);
                        window.require([
                            `https://cdn.jsdelivr.net/npm/${moduleName}@${moduleVersion}/dist/index.js`,
                        ], resolve, reject);
                    }
                    else {
                        throw err;
                    }
                };
                window.require([`${moduleName}.js`], resolve, fallback);
            }
        }).then(function (module) {
            if (module[className]) {
                return module[className];
            }
            else {
                return Promise.reject(`Class ${className} not found in module ${moduleName}@${moduleVersion}`);
            }
        });
    }
    async display_view(view) {
        var that = this;
        return Promise.resolve(view).then(function (view) {
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget.attach(view.luminoWidget, that.el);
            return view;
        });
    }
    _get_comm_info() {
        return Promise.resolve({});
    }
    _create_comm() {
        return Promise.reject('no comms available');
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (IPyWidgetsViewManager);


/***/ }),

/***/ "./lib/jupyter/lite/LiteServer.js":
/*!****************************************!*\
  !*** ./lib/jupyter/lite/LiteServer.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "startLiteServer": () => (/* binding */ startLiteServer)
/* harmony export */ });
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @datalayer/jupyterlite-server */ "webpack/sharing/consume/default/@datalayer/jupyterlite-server/@datalayer/jupyterlite-server");
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);


const serverExtensions = [
    //  import('@jupyterlite/javascript-kernel-extension'),
    __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel-extension_datalayer_jupyterli-4c7967").then(__webpack_require__.t.bind(__webpack_require__, /*! @datalayer/jupyterlite-ipykernel-extension */ "webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel-extension/@datalayer/jupyterlite-ipykernel-extension", 23)),
    __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_datalayer_jupyterlite-server-extension_datalayer_jupyterlite--eaaa26").then(__webpack_require__.t.bind(__webpack_require__, /*! @datalayer/jupyterlite-server-extension */ "webpack/sharing/consume/default/@datalayer/jupyterlite-server-extension/@datalayer/jupyterlite-server-extension", 23))
];
// custom list of disabled plugins.
const disabled = [
    '@jupyterlab/apputils-extension:workspaces',
    '@jupyterlab/application-extension:logo',
    '@jupyterlab/application-extension:main',
    '@jupyterlab/application-extension:tree-resolver',
    '@jupyterlab/apputils-extension:resolver',
    '@jupyterlab/docmanager-extension:download',
    '@jupyterlab/filebrowser-extension:download',
    '@jupyterlab/filebrowser-extension:share-file',
    '@jupyterlab/help-extension:about',
    /*
      '@jupyterlite/server-extension:contents',
      '@jupyterlite/server-extension:contents-routes',
      '@jupyterlite/server-extension:emscripten-filesystem',
      '@jupyterlite/server-extension:licenses',
      '@jupyterlite/server-extension:licenses-routes',
      '@jupyterlite/server-extension:localforage-memory-storage',
      '@jupyterlite/server-extension:localforage',
      '@jupyterlite/server-extension:nbconvert-routes',
      '@jupyterlite/server-extension:service-worker',
      '@jupyterlite/server-extension:settings',
      '@jupyterlite/server-extension:settings-routes',
      '@jupyterlite/server-extension:translation',
      '@jupyterlite/server-extension:translation-routes',
    */
];
async function startLiteServer() {
    const litePluginsToRegister = [];
    /**
     * Iterate over active plugins in an extension.
     */
    function* activePlugins(extension) {
        // Handle commonjs or es2015 modules.
        let exports;
        if (extension.hasOwnProperty('__esModule')) {
            exports = extension.default;
        }
        else {
            // CommonJS exports.
            exports = extension;
        }
        let plugins = Array.isArray(exports) ? exports : [exports];
        for (let plugin of plugins) {
            if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.Extension.isDisabled(plugin.id) ||
                disabled.includes(plugin.id) ||
                disabled.includes(plugin.id.split(':')[0])) {
                continue;
            }
            yield plugin;
        }
    }
    // Add the base serverlite extensions.
    const baseServerExtensions = await Promise.all(serverExtensions);
    baseServerExtensions.forEach(p => {
        for (let plugin of activePlugins(p)) {
            litePluginsToRegister.push(plugin);
        }
    });
    // Create the in-browser JupyterLite Server.
    const jupyterLiteServer = new _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_0__.JupyterLiteServer({});
    jupyterLiteServer.registerPluginModules(litePluginsToRegister);
    // Start the server.
    await jupyterLiteServer.start();
    // Retrieve the custom service manager from the server app.
    const { serviceManager } = jupyterLiteServer;
    return serviceManager;
}


/***/ }),

/***/ "./lib/jupyter/lumino/IPyWidgetsAttached.js":
/*!**************************************************!*\
  !*** ./lib/jupyter/lumino/IPyWidgetsAttached.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _ipywidgets_IPyWidgetsViewManager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../ipywidgets/IPyWidgetsViewManager */ "./lib/jupyter/ipywidgets/IPyWidgetsViewManager.js");


/**
 * IPyWidgetAttached allows to render a Lumino
 * Widget being mounted in the React.js tree.
 */
const IPyWidgetsAttached = (props) => {
    const { view, state } = props;
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { ref: ref => {
            if (ref) {
                var manager = new _ipywidgets_IPyWidgetsViewManager__WEBPACK_IMPORTED_MODULE_1__["default"](ref);
                manager
                    .set_state(state)
                    .then((models) => manager.create_view(models.find((element) => element.model_id === view.model_id)))
                    .then((view) => manager.display_view(view));
            }
        } }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (IPyWidgetsAttached);


/***/ }),

/***/ "./lib/jupyter/services/Services.js":
/*!******************************************!*\
  !*** ./lib/jupyter/services/Services.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Services": () => (/* binding */ Services),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
class Services {
    _serviceManager;
    constructor(services) {
        this._serviceManager = services;
    }
    kernelspecs() {
        return this._serviceManager.kernelspecs;
    }
    contents() {
        return this._serviceManager.contents;
    }
    nbconvert() {
        return this._serviceManager.nbconvert;
    }
    sessions() {
        return this._serviceManager.sessions;
    }
    settings() {
        return this._serviceManager.settings;
    }
    terminals() {
        return this._serviceManager.terminals;
    }
    workspaces() {
        return this._serviceManager.workspaces;
    }
    builder() {
        return this._serviceManager.builder;
    }
    serverSettings() {
        return this._serviceManager.serverSettings;
    }
    refreshKernelspecs() {
        return this.kernelspecs().refreshSpecs();
    }
    getKernelspecs() {
        return this.kernelspecs().specs;
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Services);


/***/ }),

/***/ "./lib/jupyter/services/kernel/Kernel.js":
/*!***********************************************!*\
  !*** ./lib/jupyter/services/kernel/Kernel.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Kernel": () => (/* binding */ Kernel),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utils_Utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils/Utils */ "./lib/utils/Utils.js");




const JUPYTER_REACT_PATH_COOKIE_NAME = "jupyter-react-kernel-path";
class Kernel {
    _clientId;
    _connectionStatus;
    _id;
    _info;
    _kernelConnection;
    _kernelManager;
    _kernelName;
    _kernelType;
    _kernelSpecName;
    _kernelSpecManager;
    _path;
    _readyResolve;
    _session;
    _sessionId;
    _sessionManager;
    _ready;
    constructor(props) {
        const { kernelManager, kernelName, kernelType, kernelSpecName, kernelModel, serverSettings } = props;
        this._kernelSpecManager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.KernelSpecManager({ serverSettings });
        this._kernelManager = kernelManager;
        this._kernelName = kernelName;
        this._kernelType = kernelType;
        this._kernelSpecName = kernelSpecName;
        this.initReady = this.initReady.bind(this);
        this.initReady();
        this.requestKernel(kernelModel);
    }
    initReady() {
        this._ready = new Promise((resolve, _) => {
            this._readyResolve = resolve;
        });
    }
    async requestKernel(kernelModel) {
        await this._kernelManager.ready;
        this._sessionManager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.SessionManager({
            kernelManager: this._kernelManager,
            serverSettings: this._kernelManager.serverSettings,
            standby: 'never',
        });
        await this._sessionManager.ready;
        if (kernelModel) {
            console.log('Reusing a pre-existing kernel model.');
            await this._sessionManager.refreshRunning();
            const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.find)(this._sessionManager.running(), (item) => {
                return item.path === this._path;
            });
            if (model) {
                this._session = this._sessionManager.connectTo({ model });
            }
        }
        else {
            let path = (0,_utils_Utils__WEBPACK_IMPORTED_MODULE_3__.getCookie)(JUPYTER_REACT_PATH_COOKIE_NAME);
            if (!path) {
                path = "kernel-" + _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                document.cookie = JUPYTER_REACT_PATH_COOKIE_NAME + "=" + path;
            }
            this._path = path;
            this._session = await this._sessionManager.startNew({
                name: this._kernelName,
                path: this._path,
                type: this._kernelType,
                kernel: {
                    name: this._kernelSpecName,
                },
            }, {
                kernelConnectionOptions: {
                    handleComms: true,
                }
            });
        }
        this._kernelConnection = this._session.kernel;
        const updateConnectionStatus = () => {
            if (this._connectionStatus === 'connected') {
                this._clientId = this._session.kernel.clientId;
                this._id = this._session.kernel.id;
                this._readyResolve();
            }
        };
        if (this._kernelConnection) {
            this._sessionId = this._session.id;
            this._connectionStatus = this._kernelConnection.connectionStatus;
            updateConnectionStatus();
            this._kernelConnection.connectionStatusChanged.connect((_, connectionStatus) => {
                //        this.initReady();
                this._connectionStatus = connectionStatus;
                updateConnectionStatus();
            });
            this._kernelConnection.info.then((info) => {
                this._info = info;
                console.log(`The default Kernel is ready`, this.toJSON());
            });
        }
    }
    get ready() {
        return this._ready;
    }
    get clientId() {
        return this._clientId;
    }
    get id() {
        return this._id;
    }
    get sessionId() {
        return this._sessionId;
    }
    get info() {
        return this._info;
    }
    get session() {
        return this._session;
    }
    get kernelManager() {
        return this._kernelManager;
    }
    get kernelSpecManager() {
        return this._kernelSpecManager;
    }
    get sessionManager() {
        return this._sessionManager;
    }
    get path() {
        return this._path;
    }
    get connection() {
        return this._kernelConnection;
    }
    toJSON() {
        return {
            path: this._path,
            id: this.id,
            clientId: this.clientId,
            sessionId: this.sessionId,
            kernelInfo: this.info,
        };
    }
    toString() {
        return `id:${this.id} - client_id:${this.clientId} - session_id:${this.sessionId} - path:${this._path}`;
    }
    shutdown() {
        this._session.kernel?.shutdown();
        this.connection?.dispose();
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Kernel);


/***/ }),

/***/ "./lib/state/redux/InitState.js":
/*!**************************************!*\
  !*** ./lib/state/redux/InitState.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InitActionType": () => (/* binding */ InitActionType),
/* harmony export */   "initActions": () => (/* binding */ initActions),
/* harmony export */   "initInitialState": () => (/* binding */ initInitialState),
/* harmony export */   "initReducer": () => (/* binding */ initReducer),
/* harmony export */   "selectStart": () => (/* binding */ selectStart)
/* harmony export */ });
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_redux__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var typescript_fsa__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! typescript-fsa */ "webpack/sharing/consume/default/typescript-fsa/typescript-fsa");
/* harmony import */ var typescript_fsa__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(typescript_fsa__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var typescript_fsa_reducers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! typescript-fsa-reducers */ "webpack/sharing/consume/default/typescript-fsa-reducers/typescript-fsa-reducers");
/* harmony import */ var typescript_fsa_reducers__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(typescript_fsa_reducers__WEBPACK_IMPORTED_MODULE_2__);



const initInitialState = {
    start: undefined,
};
/* Selectors */
const selectStart = () => (0,react_redux__WEBPACK_IMPORTED_MODULE_0__.useSelector)((state) => {
    if (state.init) {
        return state.init.start;
    }
    return initInitialState.start;
});
/* Actions */
var InitActionType;
(function (InitActionType) {
    InitActionType["GET_START"] = "jupyterReact/GET_START";
})(InitActionType || (InitActionType = {}));
const actionCreator = typescript_fsa__WEBPACK_IMPORTED_MODULE_1___default()('jupyterReact');
const initActions = {
    getStart: actionCreator(InitActionType.GET_START),
};
/* Reducers */
const initReducer = (0,typescript_fsa_reducers__WEBPACK_IMPORTED_MODULE_2__.reducerWithInitialState)(initInitialState)
    .case(initActions.getStart, (state, start) => {
    return {
        ...state,
        start,
    };
});


/***/ }),

/***/ "./lib/state/redux/Store.js":
/*!**********************************!*\
  !*** ./lib/state/redux/Store.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createInjectableStore": () => (/* binding */ createInjectableStore),
/* harmony export */   "createReduxEpicStore": () => (/* binding */ createReduxEpicStore),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! redux */ "webpack/sharing/consume/default/redux/redux");
/* harmony import */ var redux__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(redux__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var redux_observable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! redux-observable */ "webpack/sharing/consume/default/redux-observable/redux-observable");
/* harmony import */ var redux_observable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(redux_observable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _InitState__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./InitState */ "./lib/state/redux/InitState.js");



const epicMiddleware = (0,redux_observable__WEBPACK_IMPORTED_MODULE_1__.createEpicMiddleware)();
function createReducer(asyncReducers) {
    return (0,redux__WEBPACK_IMPORTED_MODULE_0__.combineReducers)({
        ...asyncReducers,
    });
}
/*
export const createEpics = (initEpics: any) => {
  const epic$ = new BehaviorSubject(initEpics);
  const rootEpic = (action$: any, state$: any, deps: any) => epic$.pipe(
    mergeMap(epic => epic(action$, state$, deps))
  );
  epicMiddleware.run(rootEpic as any);
}
*/
const createInjectableStore = (store) => {
    const injectableStore = store;
    injectableStore.asyncReducers = {};
    injectableStore.inject = (key, asyncReducer, epic) => {
        const reducer = injectableStore.asyncReducers[key];
        if (key === 'init' || !reducer) {
            if (epic) {
                epicMiddleware.run(epic);
            }
            injectableStore.asyncReducers[key] = asyncReducer;
            const newReducer = createReducer(injectableStore.asyncReducers);
            injectableStore.replaceReducer(newReducer);
        }
    };
    return injectableStore;
};
const createReduxEpicStore = () => (0,redux__WEBPACK_IMPORTED_MODULE_0__.createStore)(createReducer({ initReducer: _InitState__WEBPACK_IMPORTED_MODULE_2__.initReducer }), (0,redux__WEBPACK_IMPORTED_MODULE_0__.applyMiddleware)(epicMiddleware));
const store = createReduxEpicStore();
const injectableStore = createInjectableStore(store);
injectableStore.inject('init', _InitState__WEBPACK_IMPORTED_MODULE_2__.initReducer);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (injectableStore);


/***/ }),

/***/ "./lib/utils/Utils.js":
/*!****************************!*\
  !*** ./lib/utils/Utils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getCookie": () => (/* binding */ getCookie),
/* harmony export */   "newSourceId": () => (/* binding */ newSourceId),
/* harmony export */   "newUuid": () => (/* binding */ newUuid),
/* harmony export */   "sourceAsString": () => (/* binding */ sourceAsString)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

// const MAX = Number.MAX_SAFE_INTEGER;
// const MAX = 999999;
const newSourceId = (base) => {
    //  return base + Math.floor(Math.random() * MAX).toString();
    return base;
};
const newUuid = () => {
    return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.UUID.uuid4();
};
const sourceAsString = (cell) => {
    let source = cell.source;
    if (typeof (source) === 'object') {
        source = source.join('\n');
    }
    return source;
};
const getCookie = (name) => {
    const nameLenPlus = (name.length + 1);
    return document.cookie
        .split(';')
        .map(c => c.trim())
        .filter(cookie => {
        return cookie.substring(0, nameLenPlus) === `${name}=`;
    })
        .map(cookie => {
        return decodeURIComponent(cookie.substring(nameLenPlus));
    })[0] || null;
};


/***/ }),

/***/ "?9848":
/*!**************************************!*\
  !*** ./terminal-highlight (ignored) ***!
  \**************************************/
/***/ (() => {

/* (ignored) */

/***/ }),

/***/ "?468d":
/*!********************!*\
  !*** fs (ignored) ***!
  \********************/
/***/ (() => {

/* (ignored) */

/***/ }),

/***/ "?19bd":
/*!**********************!*\
  !*** path (ignored) ***!
  \**********************/
/***/ (() => {

/* (ignored) */

/***/ }),

/***/ "?6c7c":
/*!*******************************!*\
  !*** source-map-js (ignored) ***!
  \*******************************/
/***/ (() => {

/* (ignored) */

/***/ }),

/***/ "?37a2":
/*!*********************!*\
  !*** url (ignored) ***!
  \*********************/
/***/ (() => {

/* (ignored) */

/***/ })

}]);
//# sourceMappingURL=lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0.08c75cdca7e73b05f04c.js.map