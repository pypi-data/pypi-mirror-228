"use strict";
(self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || []).push([["lib_jupyter_lab_index_js"],{

/***/ "../../../../../node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!***************************************************************************!*\
  !*** ../../../../../node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \***************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "html {\n/*  box-sizing: content-box !important; */\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;AACA,yCAAyC;AACzC","sourcesContent":["html {\n/*  box-sizing: content-box !important; */\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!****************************************************************************!*\
  !*** ../../../../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \****************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../../../../node_modules/css-loader/dist/cjs.js!./base.css */ "../../../../../node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../../icons/react/data1/esm/ReactJsIcon.js":
/*!********************************************************!*\
  !*** ../../../../icons/react/data1/esm/ReactJsIcon.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function ReactJsIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    viewBox: "0 0 20 20",
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#61DAFB' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#61DAFB') ? 'white' : 'currentColor'),
    d: "M9.625 8.5a1.665 1.665 0 110 3.33 1.665 1.665 0 010-3.33z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#61DAFB' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#61DAFB') ? 'white' : 'currentColor'),
    d: "M15.63 7.264a12.877 12.877 0 00-.6-.19c.034-.135.065-.271.094-.409.453-2.204.157-3.98-.858-4.566-.972-.56-2.562.025-4.169 1.423-.158.137-.312.28-.463.425a11.816 11.816 0 00-.309-.285C7.642 2.167 5.954 1.538 4.941 2.124c-.97.562-1.258 2.232-.85 4.322.041.207.087.412.138.617-.238.068-.47.14-.689.217C1.564 7.968.305 9.047.305 10.165c0 1.155 1.353 2.314 3.409 3.016.166.057.334.11.504.158-.055.22-.104.442-.147.665-.39 2.053-.085 3.684.883 4.243 1.001.577 2.68-.016 4.317-1.446.129-.113.259-.233.389-.359.163.159.33.312.503.46 1.584 1.364 3.149 1.914 4.117 1.354 1-.58 1.325-2.33.903-4.461a11.1 11.1 0 00-.112-.499c.118-.034.233-.07.347-.108 2.137-.708 3.527-1.852 3.527-3.023 0-1.123-1.301-2.208-3.315-2.9zm-5.01-3.142c1.376-1.198 2.662-1.67 3.249-1.332.624.36.867 1.811.474 3.715a9.184 9.184 0 01-.083.37 19.074 19.074 0 00-2.492-.394 18.7 18.7 0 00-1.576-1.966c.14-.135.282-.266.428-.393zM5.81 11.12a23.156 23.156 0 001.113 1.923 16.932 16.932 0 01-1.718-.277c.165-.531.368-1.085.605-1.646zm-.001-1.872a17.574 17.574 0 01-.592-1.612 17.861 17.861 0 011.69-.291 23.378 23.378 0 00-1.098 1.903zm.423.936a22.386 22.386 0 011.697-2.94 22.561 22.561 0 013.397 0 25.978 25.978 0 011.702 2.93 23.707 23.707 0 01-.8 1.508c-.283.49-.582.972-.895 1.443a25.77 25.77 0 01-3.394.007 22.337 22.337 0 01-1.707-2.948zm6.685 1.896c.188-.325.368-.655.54-.989.237.536.446 1.084.626 1.642a16.93 16.93 0 01-1.738.297c.197-.313.387-.629.572-.948v-.002zm.532-2.832a26.904 26.904 0 00-1.103-1.902c.595.076 1.165.175 1.7.298a17 17 0 01-.597 1.604zM9.634 5.084c.387.423.753.865 1.096 1.324a23.217 23.217 0 00-2.202 0 17.42 17.42 0 011.106-1.324zM5.34 2.813c.624-.362 2.002.154 3.456 1.444.093.082.186.168.28.257a19.08 19.08 0 00-1.59 1.966c-.836.075-1.667.204-2.486.386-.048-.19-.09-.381-.128-.574-.351-1.79-.119-3.14.467-3.48zm-.91 9.759a10.314 10.314 0 01-.46-.144 6.743 6.743 0 01-2.174-1.155 1.644 1.644 0 01-.695-1.108c0-.679 1.011-1.544 2.699-2.133.212-.074.426-.141.641-.202.251.804.555 1.59.909 2.354a19.393 19.393 0 00-.92 2.388zm4.316 3.63a6.744 6.744 0 01-2.087 1.306 1.645 1.645 0 01-1.307.049c-.588-.34-.833-1.648-.5-3.404.04-.208.086-.414.136-.619.829.178 1.668.3 2.513.364.49.693 1.024 1.354 1.6 1.977-.116.112-.234.22-.355.326zm.909-.9c-.396-.429-.77-.877-1.122-1.343a27.807 27.807 0 002.216-.003 17.04 17.04 0 01-1.094 1.346zm4.836 1.107a1.645 1.645 0 01-.61 1.157c-.588.34-1.844-.102-3.2-1.267a11.543 11.543 0 01-.468-.427 18.69 18.69 0 001.563-1.984 18.52 18.52 0 002.524-.39c.038.154.071.304.1.451a6.72 6.72 0 01.09 2.46zm.676-3.977a7.857 7.857 0 01-.314.098 18.694 18.694 0 00-.943-2.361 18.68 18.68 0 00.907-2.327c.19.055.376.113.554.175 1.724.593 2.777 1.472 2.777 2.148 0 .721-1.136 1.656-2.981 2.267z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(ReactJsIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../../../icons/react/data2/esm/AtomSymbolIconLabIcon.js":
/*!******************************************************************!*\
  !*** ../../../../icons/react/data2/esm/AtomSymbolIconLabIcon.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/labicon */ "../../../../../node_modules/@jupyterlab/ui-components/lib/icon/labicon.js");
/* harmony import */ var _AtomSymbolIcon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./AtomSymbolIcon.svg */ "../../../../icons/react/data2/esm/AtomSymbolIcon.svg");


const atomSymbolIconLabIcon = new _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@datalayer/icons:atom-symbol',
    svgstr: _AtomSymbolIcon_svg__WEBPACK_IMPORTED_MODULE_1__,
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (atomSymbolIconLabIcon);

/***/ }),

/***/ "../../../../icons/react/data2/esm/RingedPlanetIcon.js":
/*!*************************************************************!*\
  !*** ../../../../icons/react/data2/esm/RingedPlanetIcon.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function RingedPlanetIcon({
  title,
  titleId,
  size,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    viewBox: "0 0 72 72",
    fill: "currentColor",
    "aria-hidden": "true",
    ref: svgRef,
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("circle", {
    cx: 36.146,
    cy: 36.428,
    r: 22.543,
    fill: "#ea5a47"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#d22f27",
    d: "M52.524 20.931a22.544 22.544 0 01-36.242 26.145A22.542 22.542 0 1052.524 20.93z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#f1b31c",
    d: "M52.794 22.755c7.674-.926 13.138-.024 14.191 2.849C68.825 30.622 56.51 39.754 39.478 46S7.146 53.242 5.306 48.224c-1.07-2.919 2.647-7.228 9.296-11.552l.076 1.553c-2.509 2.253-3.714 4.341-3.138 5.913 1.434 3.909 13.352 3.133 26.62-1.733S61.02 30.426 59.588 26.517c-.553-1.507-2.665-2.318-5.812-2.466z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", {
    fill: "none",
    stroke: "#000",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    strokeWidth: 2
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M17.156 46.594a21.539 21.539 0 1138.77-18.688M57.677 37.164a21.555 21.555 0 01-34.892 16.164"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M52.794 22.755c7.674-.926 13.138-.024 14.191 2.849C68.825 30.622 56.51 39.754 39.478 46S7.146 53.242 5.306 48.224c-1.07-2.919 2.647-7.228 9.296-11.552"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M53.776 24.05c3.147.15 5.259.96 5.811 2.467 1.434 3.91-8.16 11.023-21.428 15.888s-25.185 5.642-26.619 1.733c-.576-1.572.63-3.66 3.138-5.913"
  })));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(RingedPlanetIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../../../icons/react/eggs/esm/PirateSkull2Icon.js":
/*!************************************************************!*\
  !*** ../../../../icons/react/eggs/esm/PirateSkull2Icon.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function PirateSkull2Icon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    viewBox: "0 0 512 512",
    fill: colored ? 'currentColor' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('currentColor') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M256 31.203c-96 .797-117.377 76.692-79.434 135.133-6.397 6.534-10.344 15.886-.566 25.664 16 16 32 16 39.852 32.42h80.296C304 208 320 208 336 192c9.778-9.778 5.831-19.13-.566-25.664C373.377 107.896 352 32 256 31.203zm-42.146 101.049c.426-.003.862.007 1.306.03 28.404 1.442 40.84 59.718-10.83 51.095-10.412-1.738-17.355-50.963 9.524-51.125zm84.292 0c26.88.162 19.936 49.387 9.524 51.125C256 192 268.436 133.724 296.84 132.28c.444-.022.88-.032 1.306-.03zM32 144c7.406 88.586 64.475 175.544 156.623 236.797 17.959-7.251 35.767-15.322 50.424-23.877C180.254 319.737 104.939 255.465 32 144zm448 0C359.2 328.605 231.863 383.797 183.908 400.797c3.177 5.374 5.997 10.98 8.711 16.432 3.878 7.789 7.581 15.251 11.184 20.986A517.457 517.457 0 00256 417.973l.168.076a884.617 884.617 0 009.652-4.65C391.488 353.263 471.156 249.79 480 144zm-224 27.725l20.074 40.15L256 199.328l-20.074 12.547L256 171.725zm-65.604 57.11l15.76 51.042s31.268 24.92 49.844 24.92 49.844-24.92 49.844-24.92l15.76-51.041-27.086 19.236-8.063 16.248S267.35 279.547 256 279.547c-11.35 0-30.455-15.227-30.455-15.227l-8.063-16.248-27.086-19.236zm-59.984 152.976a32.548 32.548 0 00-2.375.027l.856 17.978c6.36-.302 10.814 2.416 16.11 8.64 5.298 6.222 10.32 15.707 15.24 25.589 4.918 9.882 9.707 20.12 16.122 28.45 6.415 8.327 16.202 15.446 27.969 13.89l-2.36-17.844c-4.094.541-6.78-1.099-11.349-7.031-4.57-5.933-9.275-15.46-14.268-25.489-4.992-10.029-10.297-20.604-17.644-29.234-6.888-8.09-16.556-14.686-28.3-14.976zm251.176 0c-11.745.29-21.413 6.885-28.3 14.976-7.348 8.63-12.653 19.205-17.645 29.234-4.993 10.03-9.698 19.556-14.268 25.489-4.57 5.932-7.255 7.572-11.35 7.031l-2.359 17.844c11.767 1.556 21.554-5.563 27.969-13.89 6.415-8.33 11.204-18.568 16.123-28.45 4.919-9.882 9.94-19.367 15.238-25.59 5.297-6.223 9.75-8.941 16.111-8.639l.856-17.978a32.853 32.853 0 00-2.375-.027zm-55.928 18.107c-13.97 10.003-30.13 18.92-47.424 27.478a524.868 524.868 0 0029.961 10.819c3.603-5.735 7.306-13.197 11.184-20.986 2.714-5.453 5.534-11.058 8.71-16.432-.77-.273-1.62-.586-2.43-.879zm-191.808 23.371l-27.67 10.352 7.904 31.771 36.424-11.707c-1.418-2.814-2.81-5.649-4.207-8.457-4.048-8.131-8.169-15.961-12.451-21.959zm244.296 0c-4.282 5.998-8.403 13.828-12.45 21.959-1.399 2.808-2.79 5.643-4.208 8.457l36.424 11.707 7.904-31.771-27.67-10.352zM78.271 435.438a9.632 9.632 0 00-1.32.12 6.824 6.824 0 00-1.217.313c-11.544 4.201-25.105 18.04-21.648 29.828 3.07 10.472 19.675 13.359 30.492 11.916 3.828-.51 8.415-3.761 12.234-7.086l-8.124-32.648c-3.238-1.285-7.214-2.528-10.417-2.443zm355.458 0c-3.203-.085-7.179 1.158-10.416 2.443l-8.125 32.648c3.819 3.325 8.406 6.576 12.234 7.086 10.817 1.443 27.422-1.444 30.492-11.916 3.457-11.788-10.104-25.627-21.648-29.828a6.824 6.824 0 00-1.217-.312 9.632 9.632 0 00-1.32-.122z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(PirateSkull2Icon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "./lib/app/JupyterReact.js":
/*!*********************************!*\
  !*** ./lib/app/JupyterReact.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/ThemeProvider.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/BaseStyles.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/UnderlineNav/index.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @datalayer/icons-react */ "../../../../icons/react/data2/esm/RingedPlanetIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @datalayer/icons-react */ "../../../../icons/react/data1/esm/ReactJsIcon.js");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tabs_AboutTab__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/AboutTab */ "./lib/app/tabs/AboutTab.js");
/* harmony import */ var _tabs_ComponentsTab__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/ComponentsTab */ "./lib/app/tabs/ComponentsTab.js");
/* harmony import */ var _jupyter_JupyterHandlers__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../jupyter/JupyterHandlers */ "./lib/jupyter/JupyterHandlers.js");









const JupyterReact = (props) => {
    const { app } = props;
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    const [version, setVersion] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyter_JupyterHandlers__WEBPACK_IMPORTED_MODULE_3__.requestAPI)(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings(), 'jupyter_react', 'config')
            .then(data => {
            setVersion(data.version);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_react extension.\n${reason}`);
        });
    });
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { style: { maxWidth: 700 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { mb: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav, { "aria-label": "jupyter-react", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-current": "page", icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__["default"], onSelect: e => { e.preventDefault(); setTab(1); }, children: "Components" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_9__["default"], onSelect: e => { e.preventDefault(); setTab(2); }, children: "About" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { m: 3, children: [(tab === 1) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_ComponentsTab__WEBPACK_IMPORTED_MODULE_10__["default"], { app: app }), (tab === 2) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_AboutTab__WEBPACK_IMPORTED_MODULE_11__["default"], { version: version })] })] }) }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JupyterReact);


/***/ }),

/***/ "./lib/app/tabs/AboutTab.js":
/*!**********************************!*\
  !*** ./lib/app/tabs/AboutTab.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Pagehead/Pagehead.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Label/Label.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Link/Link.js");
/* harmony import */ var _datalayer_icons_react_eggs_PirateSkull2Icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/icons-react/eggs/PirateSkull2Icon */ "../../../../icons/react/eggs/esm/PirateSkull2Icon.js");




const AboutTab = (props) => {
    const { version } = props;
    const [pirate, setPirate] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { as: "h3", children: ["Jupyter React", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { marginLeft: 1 }, children: version })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: "\uD83E\uDE90 \u269B\uFE0F React.js components \uD83D\uDCAF% compatible with Jupyter." }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { mt: 3, children: !pirate ?
                    (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("img", { src: "https://assets.datalayer.tech/releases/0.2.0-omalley.png", onClick: e => setPirate(true) })
                    :
                        (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_eggs_PirateSkull2Icon__WEBPACK_IMPORTED_MODULE_6__["default"], { size: 500, onClick: e => setPirate(false) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://datalayer.tech/docs/releases/0.2.0-omalley", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "O'Malley release" }) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://github.com/datalayer/jupyter-ui/tree/main/packages/react", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "Source code" }) }) })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AboutTab);


/***/ }),

/***/ "./lib/app/tabs/ComponentsTab.js":
/*!***************************************!*\
  !*** ./lib/app/tabs/ComponentsTab.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../../../node_modules/@primer/react/lib-esm/NavList/NavList.js");
/* harmony import */ var _components_FileBrowserComponent__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/FileBrowserComponent */ "./lib/app/tabs/components/FileBrowserComponent.js");
/* harmony import */ var _components_CellComponent__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/CellComponent */ "./lib/app/tabs/components/CellComponent.js");
/* harmony import */ var _components_NotebookComponent__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/NotebookComponent */ "./lib/app/tabs/components/NotebookComponent.js");
/* harmony import */ var _components_IPyWidgetsComponent__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/IPyWidgetsComponent */ "./lib/app/tabs/components/IPyWidgetsComponent.js");







const MainTab = (props) => {
    const [nav, setNav] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { sx: { display: 'flex' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.NavList, { sx: {
                            '> *': {
                                paddingTop: '0px'
                            }
                        }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.NavList.Item, { "aria-current": nav === 1 ? 'page' : undefined, onClick: e => setNav(1), children: "File Browser" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.NavList.Item, { "aria-current": nav === 2 ? 'page' : undefined, onClick: e => setNav(2), children: "Cell" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.NavList.Item, { "aria-current": nav === 3 ? 'page' : undefined, onClick: e => setNav(3), children: "Notebook" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.NavList.Item, { "aria-current": nav === 4 ? 'page' : undefined, onClick: e => setNav(4), children: "IPyWidgets" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { ml: 3, sx: { width: '100%' }, children: [(nav === 1) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_FileBrowserComponent__WEBPACK_IMPORTED_MODULE_4__["default"], {}), (nav === 2) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_CellComponent__WEBPACK_IMPORTED_MODULE_5__["default"], {}), (nav === 3) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_NotebookComponent__WEBPACK_IMPORTED_MODULE_6__["default"], {}), (nav === 4) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_IPyWidgetsComponent__WEBPACK_IMPORTED_MODULE_7__["default"], {})] })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MainTab);


/***/ }),

/***/ "./lib/app/tabs/components/CellComponent.js":
/*!**************************************************!*\
  !*** ./lib/app/tabs/components/CellComponent.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../jupyter/Jupyter */ "./lib/jupyter/Jupyter.js");


// import Cell from '../../../components/cell/Cell';
const CellComponent = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__.Jupyter, {}) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CellComponent);


/***/ }),

/***/ "./lib/app/tabs/components/FileBrowserComponent.js":
/*!*********************************************************!*\
  !*** ./lib/app/tabs/components/FileBrowserComponent.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../jupyter/Jupyter */ "./lib/jupyter/Jupyter.js");
/* harmony import */ var _components_filebrowser_FileBrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../components/filebrowser/FileBrowser */ "./lib/components/filebrowser/FileBrowser.js");



const FileBrowserComponent = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__.Jupyter, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_filebrowser_FileBrowser__WEBPACK_IMPORTED_MODULE_2__.FileBrowser, {}) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FileBrowserComponent);


/***/ }),

/***/ "./lib/app/tabs/components/IPyWidgetsComponent.js":
/*!********************************************************!*\
  !*** ./lib/app/tabs/components/IPyWidgetsComponent.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../jupyter/Jupyter */ "./lib/jupyter/Jupyter.js");
/* harmony import */ var _components_output_OutputIPyWidgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../components/output/OutputIPyWidgets */ "./lib/components/output/OutputIPyWidgets.js");
/* harmony import */ var _examples_notebooks_OutputIPyWidgetsExample__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../../examples/notebooks/OutputIPyWidgetsExample */ "./lib/examples/notebooks/OutputIPyWidgetsExample.js");




const IPyWidgetsComponent = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__.Jupyter, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_output_OutputIPyWidgets__WEBPACK_IMPORTED_MODULE_2__["default"], { view: _examples_notebooks_OutputIPyWidgetsExample__WEBPACK_IMPORTED_MODULE_3__.view, state: _examples_notebooks_OutputIPyWidgetsExample__WEBPACK_IMPORTED_MODULE_3__.state }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (IPyWidgetsComponent);


/***/ }),

/***/ "./lib/app/tabs/components/NotebookComponent.js":
/*!******************************************************!*\
  !*** ./lib/app/tabs/components/NotebookComponent.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../jupyter/Jupyter */ "./lib/jupyter/Jupyter.js");


// import Notebook from '../../../components/notebook/Notebook';
// import CellSidebarNew from "../../../components/notebook/cell/sidebar/CellSidebarNew";
const NotebookComponent = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_jupyter_Jupyter__WEBPACK_IMPORTED_MODULE_1__.Jupyter, {}) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (NotebookComponent);


/***/ }),

/***/ "./lib/components/notebook/cell/prompt/CountdownOutputPrompt.js":
/*!**********************************************************************!*\
  !*** ./lib/components/notebook/cell/prompt/CountdownOutputPrompt.js ***!
  \**********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CountdownOutputPrompt": () => (/* binding */ CountdownOutputPrompt),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Countdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Countdown */ "./lib/components/notebook/cell/prompt/Countdown.js");



const OUTPUT_PROMPT_CLASS = 'jp-OutputPrompt';
class CountdownOutputPrompt extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _executionCount = null;
    state = {
        count: 100
    };
    constructor() {
        super();
        this.addClass(OUTPUT_PROMPT_CLASS);
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
            this.state = {
                count: Number(value)
            };
            this.update();
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CountdownOutputPrompt);


/***/ }),

/***/ "./lib/examples/notebooks/OutputIPyWidgetsExample.js":
/*!***********************************************************!*\
  !*** ./lib/examples/notebooks/OutputIPyWidgetsExample.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "state": () => (/* binding */ state),
/* harmony export */   "view": () => (/* binding */ view)
/* harmony export */ });
const view = {
    "version_major": 2,
    "version_minor": 0,
    "model_id": "8621699ecc804983a612f09b7dfe806b"
};
const state = {
    "version_major": 2,
    "version_minor": 0,
    "state": {
        "8621699ecc804983a612f09b7dfe806b": {
            "model_name": "VBoxModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "_view_module_version": "1.0.0",
                "children": [
                    "IPY_MODEL_a8b1ae50aada4d929397b907115bfc2c",
                    "IPY_MODEL_289e54d14b7c4c6d8ac18b4c86ab514c",
                    "IPY_MODEL_965bbfeaddd74b9baa488c7f6ac13027"
                ],
                "_model_module_version": "1.0.0",
                "layout": "IPY_MODEL_d7d14e74f61f4b3bb5f53a713bcadced",
                "_view_count": 1
            }
        },
        "961d612211fe4c64a70f48942d885c14": {
            "model_name": "LayoutModel",
            "model_module": "@jupyter-widgets/base",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "564e75ddea4c4ea0a32c4bd39ed0ed6d": {
            "model_name": "SliderStyleModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "a8b1ae50aada4d929397b907115bfc2c": {
            "model_name": "IntSliderModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "style": "IPY_MODEL_564e75ddea4c4ea0a32c4bd39ed0ed6d",
                "_view_module_version": "1.0.0",
                "max": 200,
                "value": 100,
                "_model_module_version": "1.0.0",
                "layout": "IPY_MODEL_961d612211fe4c64a70f48942d885c14",
                "_view_count": 1
            }
        },
        "b63481ca8b7943aa85d097a114a931f5": {
            "model_name": "LayoutModel",
            "model_module": "@jupyter-widgets/base",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "d86e0cb348eb48bf97f14906a9406731": {
            "model_name": "SliderStyleModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "289e54d14b7c4c6d8ac18b4c86ab514c": {
            "model_name": "IntSliderModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "style": "IPY_MODEL_d86e0cb348eb48bf97f14906a9406731",
                "_view_module_version": "1.0.0",
                "value": 40,
                "_model_module_version": "1.0.0",
                "layout": "IPY_MODEL_b63481ca8b7943aa85d097a114a931f5",
                "_view_count": 1
            }
        },
        "bb589d8dc365404b94e73a153407128f": {
            "model_name": "LayoutModel",
            "model_module": "@jupyter-widgets/base",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "19a24d8ea5a248be8db79790290ae2a1": {
            "model_name": "ButtonStyleModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        },
        "965bbfeaddd74b9baa488c7f6ac13027": {
            "model_name": "ButtonModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "style": "IPY_MODEL_19a24d8ea5a248be8db79790290ae2a1",
                "_view_module_version": "1.0.0",
                "icon": "legal",
                "_model_module_version": "1.0.0",
                "layout": "IPY_MODEL_bb589d8dc365404b94e73a153407128f",
                "_view_count": 1
            }
        },
        "6edd9d3360cc47c8aceff0ba11edeca9": {
            "model_name": "DirectionalLinkModel",
            "model_module": "@jupyter-widgets/controls",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "target": ["IPY_MODEL_289e54d14b7c4c6d8ac18b4c86ab514c", "max"],
                "source": ["IPY_MODEL_a8b1ae50aada4d929397b907115bfc2c", "value"],
                "_view_module_version": "1.0.0",
                "_view_name": ""
            }
        },
        "d7d14e74f61f4b3bb5f53a713bcadced": {
            "model_name": "LayoutModel",
            "model_module": "@jupyter-widgets/base",
            "model_module_version": "1.0.0",
            "state": {
                "_model_module_version": "1.0.0",
                "_view_module_version": "1.0.0",
                "_view_count": 1
            }
        }
    }
};


/***/ }),

/***/ "./lib/jupyter/lab/index.js":
/*!**********************************!*\
  !*** ./lib/jupyter/lab/index.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _datalayer_icons_react_data2_AtomSymbolIconLabIcon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react/data2/AtomSymbolIconLabIcon */ "../../../../icons/react/data2/esm/AtomSymbolIconLabIcon.js");
/* harmony import */ var _JupyterHandlers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../JupyterHandlers */ "./lib/jupyter/JupyterHandlers.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/jupyter/lab/widget.js");
/* harmony import */ var _notebook_content_plugin__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./notebook/content/plugin */ "./lib/jupyter/lab/notebook/content/plugin.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../style/index.css */ "./style/index.css");









/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-jupyter-react-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/jupyter-react extension.
 */
const jupyterReactPlugin = {
    id: '@datalayer/jupyter-react:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    activate: (app, palette, settingRegistry, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Show Jupyter React',
            label: 'Jupyter React',
            icon: _datalayer_icons_react_data2_AtomSymbolIconLabIcon__WEBPACK_IMPORTED_MODULE_5__["default"],
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_6__.JupyterReactWidget(app);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.title.label = 'Jupyter React';
                widget.title.icon = _datalayer_icons_react_data2_AtomSymbolIconLabIcon__WEBPACK_IMPORTED_MODULE_5__["default"];
                app.shell.add(widget, 'main');
            }
        });
        const category = 'Jupyter React';
        palette.addItem({ command, category, args: { origin: 'from palette' } });
        if (launcher) {
            launcher.add({
                command,
                category: 'Datalayer',
                rank: 4,
            });
        }
        if (settingRegistry) {
            settingRegistry
                .load(jupyterReactPlugin.id)
                .then(settings => {
                console.log('@datalayer/jupyter-react settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/jupyter-react.', reason);
            });
        }
        (0,_JupyterHandlers__WEBPACK_IMPORTED_MODULE_7__.requestAPI)(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings(), 'jupyter_react', 'config')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The Jupyter Server jupyter_react extension extension.\n${reason}`);
        });
        console.log('JupyterLab plugin @datalayer/jupyter-react is activated.');
    }
};
const plugins = [
    jupyterReactPlugin,
    _notebook_content_plugin__WEBPACK_IMPORTED_MODULE_8__["default"],
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/jupyter/lab/notebook/content/CountdownContentFactory.js":
/*!*********************************************************************!*\
  !*** ./lib/jupyter/lab/notebook/content/CountdownContentFactory.js ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CountdownContentFactory": () => (/* binding */ CountdownContentFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_notebook_cell_prompt_CountdownInputPrompt__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../components/notebook/cell/prompt/CountdownInputPrompt */ "./lib/components/notebook/cell/prompt/CountdownInputPrompt.js");
/* harmony import */ var _components_notebook_cell_prompt_CountdownOutputPrompt__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../components/notebook/cell/prompt/CountdownOutputPrompt */ "./lib/components/notebook/cell/prompt/CountdownOutputPrompt.js");



class CountdownContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    constructor(options) {
        super(options);
    }
    /** @override */
    createInputPrompt() {
        return new _components_notebook_cell_prompt_CountdownInputPrompt__WEBPACK_IMPORTED_MODULE_1__["default"]();
    }
    /** @override */
    createOutputPrompt() {
        return new _components_notebook_cell_prompt_CountdownOutputPrompt__WEBPACK_IMPORTED_MODULE_2__["default"]();
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CountdownContentFactory);


/***/ }),

/***/ "./lib/jupyter/lab/notebook/content/plugin.js":
/*!****************************************************!*\
  !*** ./lib/jupyter/lab/notebook/content/plugin.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _CountdownContentFactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./CountdownContentFactory */ "./lib/jupyter/lab/notebook/content/CountdownContentFactory.js");



/**
 * The notebook cell factory provider.
 */
const contentFactoryPlugin = {
    id: '@datalayer/jupyter-react:notebook-content-factory',
    description: 'Provides the notebook cell factory.',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _CountdownContentFactory__WEBPACK_IMPORTED_MODULE_2__["default"]({ editorFactory });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (contentFactoryPlugin);


/***/ }),

/***/ "./lib/jupyter/lab/widget.js":
/*!***********************************!*\
  !*** ./lib/jupyter/lab/widget.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterReactWidget": () => (/* binding */ JupyterReactWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _app_JupyterReact__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../app/JupyterReact */ "./lib/app/JupyterReact.js");



class JupyterReactWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _app;
    constructor(app) {
        super();
        this._app = app;
        this.addClass('dla-Container');
    }
    render() {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_app_JupyterReact__WEBPACK_IMPORTED_MODULE_2__["default"], { app: this._app });
    }
}


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../../../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../../../../icons/react/data2/esm/AtomSymbolIcon.svg":
/*!************************************************************!*\
  !*** ../../../../icons/react/data2/esm/AtomSymbolIcon.svg ***!
  \************************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 72 72\" fill=\"currentColor\" aria-hidden=\"true\">\n  <g fill=\"#92D3F5\" stroke=\"#92D3F5\" stroke-linejoin=\"round\" stroke-miterlimit=\"10\">\n    <path stroke-width=\"1.8\" d=\"M28.127 22.764a69.81 69.81 0 00-.848 7.426c-3.347 1.87-6.345 3.846-8.867 5.81-6.16-4.8-9.46-9.53-8.077-12.435 1.57-3.3 8.693-3.405 17.792-.801zM62.642 48.435c-1.57 3.3-8.693 3.405-17.804.802a76.329 76.329 0 01-8.344-2.952 75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673 85.79 85.79 0 010-11.632 89.391 89.391 0 015.171-2.673 75.948 75.948 0 014.044-1.801 91.833 91.833 0 014.033 1.8 82.302 82.302 0 015.16 2.662 85.923 85.923 0 010 11.656c3.358-1.883 6.356-3.858 8.878-5.834 6.16 4.8 9.46 9.53 8.077 12.435z\"/>\n    <path stroke-width=\"1.8\" d=\"M44.838 49.236c-1.545 9.344-4.706 15.724-8.355 15.724-3.65 0-6.81-6.38-8.356-15.724 2.65-.755 5.462-1.743 8.367-2.951a76.315 76.315 0 008.344 2.951zM44.838 22.764a76.329 76.329 0 00-8.344 2.951c-2.905-1.208-5.717-2.196-8.367-2.951C29.684 13.42 32.834 7.04 36.483 7.04s6.798 6.38 8.355 15.724z\"/>\n    <path stroke-width=\"2\" d=\"M36.494 25.715a75.948 75.948 0 00-4.044 1.802 89.359 89.359 0 00-5.171 2.673 69.81 69.81 0 01.848-7.426c2.65.755 5.462 1.743 8.367 2.951z\"/>\n    <path stroke-width=\"2\" d=\"M45.884 36c0 1.999-.07 3.951-.197 5.834a69.407 69.407 0 01-.849 7.402 76.329 76.329 0 01-8.344-2.951 75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673 85.79 85.79 0 010-11.633 89.391 89.391 0 015.171-2.672 75.948 75.948 0 014.044-1.802 91.833 91.833 0 014.033 1.802 82.302 82.302 0 015.16 2.66c.127 1.883.197 3.824.197 5.823z\"/>\n    <path stroke-width=\"2\" d=\"M36.494 46.285c-2.905 1.208-5.717 2.196-8.367 2.951a69.582 69.582 0 01-.848-7.414 89.391 89.391 0 005.171 2.673c1.36.65 2.708 1.244 4.044 1.79z\"/>\n    <path stroke-width=\"1.8\" d=\"M28.127 49.236c-9.11 2.604-16.223 2.487-17.792-.801-1.383-2.906 1.918-7.636 8.077-12.435 2.522 1.976 5.52 3.951 8.867 5.822.162 2.615.453 5.113.848 7.414z\"/>\n    <path stroke-width=\"2\" d=\"M27.081 36c0 1.999.07 3.94.198 5.822-3.347-1.87-6.345-3.846-8.867-5.822 2.522-1.964 5.52-3.94 8.867-5.81A85.441 85.441 0 0027.08 36zM45.687 30.178a82.302 82.302 0 00-5.16-2.661 91.833 91.833 0 00-4.033-1.802 76.329 76.329 0 018.344-2.952c.395 2.302.686 4.8.849 7.415z\"/>\n    <path stroke-width=\"1.8\" d=\"M54.565 36c-2.522-1.964-5.52-3.94-8.878-5.822a69.64 69.64 0 00-.849-7.414c9.111-2.604 16.235-2.499 17.804.801 1.383 2.906-1.918 7.636-8.077 12.435z\"/>\n    <path stroke-width=\"2\" d=\"M45.687 41.834a86.268 86.268 0 000-11.656c3.358 1.882 6.356 3.858 8.878 5.822-2.522 1.976-5.52 3.951-8.878 5.834z\"/>\n    <path stroke-width=\"2\" d=\"M45.884 36c0 1.999-.07 3.951-.197 5.834a82.302 82.302 0 01-5.16 2.661 91.419 91.419 0 01-4.033 1.79 75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673 85.79 85.79 0 010-11.633 89.391 89.391 0 015.171-2.672 75.948 75.948 0 014.044-1.802 91.833 91.833 0 014.033 1.802 82.302 82.302 0 015.16 2.66c.127 1.883.197 3.824.197 5.823z\"/>\n  </g>\n  <g fill=\"none\" stroke=\"#000\" stroke-miterlimit=\"10\" stroke-width=\"2\">\n    <path stroke-linejoin=\"round\" d=\"M18.412 36c-6.16-4.8-9.46-9.53-8.077-12.435 1.57-3.3 8.693-3.405 17.792-.802M54.565 36c6.16 4.8 9.46 9.53 8.077 12.435-1.57 3.3-8.693 3.405-17.804.802a76.329 76.329 0 01-8.344-2.952 75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M44.092 53c-1.7 7.251-4.474 11.96-7.61 11.96-3.648 0-6.81-6.38-8.355-15.723l-.484-2.346M28.927 18.79c1.709-7.132 4.451-11.75 7.556-11.75 3.649 0 6.798 6.38 8.355 15.724\"/>\n    <path stroke-linejoin=\"round\" d=\"M28.127 22.764c2.65.755 5.462 1.743 8.367 2.951M44.838 49.236a76.329 76.329 0 01-8.344-2.951 75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M45.868 34.35a85.73 85.73 0 01-.181 7.484c-.054.857-.12 1.7-.2 2.528M23.718 50.317c-6.937 1.394-12.078.854-13.383-1.882-1.106-2.323.782-5.812 4.731-9.57\"/>\n    <path stroke-linejoin=\"round\" d=\"M27.134 41.74c-3.289-1.846-6.237-3.793-8.722-5.74M27.279 41.822a94.588 94.588 0 01-.145-.081\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M44.838 22.764c.138.803.263 1.63.375 2.477M49.13 21.706c7-1.426 12.2-.902 13.512 1.86 1.063 2.234-.644 5.549-4.292 9.144M54.565 36c-2.522-1.964-5.52-3.94-8.878-5.822\"/>\n    <path stroke-linejoin=\"round\" d=\"M45.687 30.178c3.358 1.882 6.356 3.858 8.878 5.822\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M41.666 43.947c-.282.14-.568.279-.858.415\"/>\n    <path stroke-linejoin=\"round\" d=\"M36.494 25.715a91.833 91.833 0 014.033 1.802 82.302 82.302 0 015.16 2.66\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M27.09 36.722a152.3 152.3 0 01.189-9.427\"/>\n    <path stroke-linejoin=\"round\" d=\"M36.494 46.285a75.65 75.65 0 01-4.044-1.79 89.359 89.359 0 01-5.171-2.673\"/>\n    <circle cx=\"36.826\" cy=\"36.327\" r=\"3.263\"/>\n    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M31.61 48.364s.338-.06.97-.329M49.702 39.967s1.404-.897 1.646-1.103M31.707 27.295c-.283.143-.566.291-.849.443M22.221 32.767s.228-.238.814-.589M39.752 23.202s1.615-.59 1.945-.661\"/>\n  </g>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_jupyter_lab_index_js.2ad407681386fad9f5cf.js.map