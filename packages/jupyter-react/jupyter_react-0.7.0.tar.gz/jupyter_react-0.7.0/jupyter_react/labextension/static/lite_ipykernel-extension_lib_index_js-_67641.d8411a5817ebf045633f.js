"use strict";
(self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || []).push([["lite_ipykernel-extension_lib_index_js-_67641"],{

/***/ "../lite/ipykernel-extension/lib/index.js":
/*!************************************************!*\
  !*** ../lite/ipykernel-extension/lib/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @datalayer/jupyterlite-server */ "webpack/sharing/consume/default/@datalayer/jupyterlite-server/@datalayer/jupyterlite-server");
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "webpack/sharing/consume/default/@datalayer/jupyterlite-kernel/@datalayer/jupyterlite-kernel");
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The default CDN fallback for Pyodide
 */
const PYODIDE_CDN_URL = 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js';
/**
 * The id for the extension, and key in the litePlugins.
 */
const PLUGIN_ID = '@datalayer/jupyterlite-ipykernel-extension:kernel';
/**
 * A plugin to register the Pyodide kernel.
 */
const kernel = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__.IKernelSpecs, _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_1__.IServiceWorkerRegistrationWrapper],
    activate: (app, kernelspecs, serviceWorkerRegistrationWrapper) => {
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getBaseUrl();
        const config = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('litePluginSettings') || '{}')[PLUGIN_ID] || {};
        const url = config.pyodideUrl || PYODIDE_CDN_URL;
        const pyodideUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.parse(url).href;
        const rawPipUrls = config.pipliteUrls || [];
        const pipliteUrls = rawPipUrls.map((pipUrl) => _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.parse(pipUrl).href);
        const disablePyPIFallback = !!config.disablePyPIFallback;
        kernelspecs.register({
            spec: {
                name: 'python',
                display_name: 'Python (Pyodide)',
                language: 'python',
                argv: [],
                resources: {
                    'logo-32x32': 'TODO',
                    'logo-64x64': _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(baseUrl, '/kernelspecs/python.png'),
                },
            },
            create: async (options) => {
                const { PyoliteKernel } = await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel_datalayer_jupyterlite-ipykernel").then(__webpack_require__.t.bind(__webpack_require__, /*! @datalayer/jupyterlite-ipykernel */ "webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel/@datalayer/jupyterlite-ipykernel", 23));
                return new PyoliteKernel({
                    ...options,
                    pyodideUrl,
                    pipliteUrls,
                    disablePyPIFallback,
                    mountDrive: serviceWorkerRegistrationWrapper.enabled,
                });
            },
        });
    },
};
const plugins = [kernel];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lite_ipykernel-extension_lib_index_js-_67641.d8411a5817ebf045633f.js.map