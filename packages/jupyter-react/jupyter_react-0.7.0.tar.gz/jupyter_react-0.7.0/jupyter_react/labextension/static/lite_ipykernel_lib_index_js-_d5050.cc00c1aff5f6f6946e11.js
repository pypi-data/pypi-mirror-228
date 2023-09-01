"use strict";
(self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || []).push([["lite_ipykernel_lib_index_js-_d5050"],{

/***/ "../lite/ipykernel/lib/_pypi.js":
/*!**************************************!*\
  !*** ../lite/ipykernel/lib/_pypi.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PIPLITE_WHEEL": () => (/* binding */ PIPLITE_WHEEL)
/* harmony export */ });
// export * as allJSONUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/all.json';
// export * as ipykernelWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/ipykernel-6.9.2-py3-none-any.whl';
// export * as pipliteWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/piplite-0.1.0b11-py3-none-any.whl';
// export * as pyoliteWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/pyolite-0.1.0b11-py3-none-any.whl';
// export * as widgetsnbextensionWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/widgetsnbextension-3.6.0-py3-none-any.whl';
const PIPLITE_WHEEL = 'piplite-0.1.0b11-py3-none-any.whl';


/***/ }),

/***/ "../lite/ipykernel/lib/index.js":
/*!**************************************!*\
  !*** ../lite/ipykernel/lib/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PIPLITE_WHEEL": () => (/* reexport safe */ _pypi__WEBPACK_IMPORTED_MODULE_0__.PIPLITE_WHEEL),
/* harmony export */   "PyoliteKernel": () => (/* reexport safe */ _kernel__WEBPACK_IMPORTED_MODULE_1__.PyoliteKernel),
/* harmony export */   "PyoliteRemoteKernel": () => (/* reexport safe */ _worker__WEBPACK_IMPORTED_MODULE_2__.PyoliteRemoteKernel)
/* harmony export */ });
/* harmony import */ var _pypi__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./_pypi */ "../lite/ipykernel/lib/_pypi.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./kernel */ "../lite/ipykernel/lib/kernel.js");
/* harmony import */ var _worker__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./worker */ "../lite/ipykernel/lib/worker.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/***/ }),

/***/ "../lite/ipykernel/lib/kernel.js":
/*!***************************************!*\
  !*** ../lite/ipykernel/lib/kernel.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PyoliteKernel": () => (/* binding */ PyoliteKernel)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "webpack/sharing/consume/default/@datalayer/jupyterlite-kernel/@datalayer/jupyterlite-kernel");
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var comlink__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! comlink */ "../../../../../node_modules/comlink/dist/esm/comlink.mjs");
/* harmony import */ var _pypi__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./_pypi */ "../lite/ipykernel/lib/_pypi.js");





/**
 * A kernel that executes Python code with Pyodide.
 */
class PyoliteKernel extends _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__.BaseKernel {
    /**
     * Instantiate a new PyodideKernel
     *
     * @param options The instantiation options for a new PyodideKernel
     */
    constructor(options) {
        super(options);
        this._worker = this.initWorker(options);
        this._worker.onmessage = (e) => this._processWorkerMessage(e.data);
        this._remoteKernel = this.initRemote(options);
        this._ready.resolve();
    }
    /**
     * Load the worker.
     *
     * ### Note
     *
     * Subclasses must implement this typographically almost _exactly_ for
     * webpack to find it.
     */
    initWorker(options) {
        return new Worker(new URL(/* worker import */ __webpack_require__.p + __webpack_require__.u("lite_ipykernel_lib_comlink_worker_js"), __webpack_require__.b), {
            type: undefined,
        });
    }
    initRemote(options) {
        const remote = (0,comlink__WEBPACK_IMPORTED_MODULE_3__.wrap)(this._worker);
        const remoteOptions = this.initRemoteOptions(options);
        remote.initialize(remoteOptions);
        return remote;
    }
    initRemoteOptions(options) {
        const { pyodideUrl } = options;
        const indexUrl = pyodideUrl.slice(0, pyodideUrl.lastIndexOf('/') + 1);
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl();
        //    const pypi = URLExt.join(baseUrl, 'build/pypi');
        const pypi = "https://datalayer-assets.s3.us-west-2.amazonaws.com/pypi";
        const pipliteUrls = [...(options.pipliteUrls || []), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(pypi, 'all.json')];
        const pipliteWheelUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(pypi, _pypi__WEBPACK_IMPORTED_MODULE_4__.PIPLITE_WHEEL);
        const disablePyPIFallback = !!options.disablePyPIFallback;
        return {
            baseUrl,
            pyodideUrl,
            indexUrl,
            pipliteWheelUrl,
            pipliteUrls,
            disablePyPIFallback,
            location: this.location,
            mountDrive: options.mountDrive,
        };
    }
    /**
     * Dispose the kernel.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._worker.terminate();
        this._worker = null;
        super.dispose();
    }
    /**
     * A promise that is fulfilled when the kernel is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Process a message coming from the pyodide web worker.
     *
     * @param msg The worker message to process.
     */
    _processWorkerMessage(msg) {
        if (!msg.type) {
            return;
        }
        switch (msg.type) {
            case 'stream': {
                const bundle = msg.bundle ?? { name: 'stdout', text: '' };
                this.stream(bundle, msg.parentHeader);
                break;
            }
            case 'input_request': {
                const bundle = msg.content ?? { prompt: '', password: false };
                this.inputRequest(bundle, msg.parentHeader);
                break;
            }
            case 'display_data': {
                const bundle = msg.bundle ?? { data: {}, metadata: {}, transient: {} };
                this.displayData(bundle, msg.parentHeader);
                break;
            }
            case 'update_display_data': {
                const bundle = msg.bundle ?? { data: {}, metadata: {}, transient: {} };
                this.updateDisplayData(bundle, msg.parentHeader);
                break;
            }
            case 'clear_output': {
                const bundle = msg.bundle ?? { wait: false };
                this.clearOutput(bundle, msg.parentHeader);
                break;
            }
            case 'execute_result': {
                const bundle = msg.bundle ?? { execution_count: 0, data: {}, metadata: {} };
                this.publishExecuteResult(bundle, msg.parentHeader);
                break;
            }
            case 'execute_error': {
                const bundle = msg.bundle ?? { ename: '', evalue: '', traceback: [] };
                this.publishExecuteError(bundle, msg.parentHeader);
                break;
            }
            case 'comm_msg':
            case 'comm_open':
            case 'comm_close': {
                this.handleComm(msg.type, msg.content, msg.metadata, msg.buffers, msg.parentHeader);
                break;
            }
        }
    }
    /**
     * Handle a kernel_info_request message
     */
    async kernelInfoRequest() {
        const content = {
            implementation: 'pyodide',
            implementation_version: '0.1.0',
            language_info: {
                codemirror_mode: {
                    name: 'python',
                    version: 3,
                },
                file_extension: '.py',
                mimetype: 'text/x-python',
                name: 'python',
                nbconvert_exporter: 'python',
                pygments_lexer: 'ipython3',
                version: '3.8',
            },
            protocol_version: '5.3',
            status: 'ok',
            banner: 'Pyolite: A WebAssembly-powered Python kernel backed by Pyodide',
            help_links: [
                {
                    text: 'Python (WASM) Kernel',
                    url: 'https://pyodide.org',
                },
            ],
        };
        return content;
    }
    /**
     * Handle an `execute_request` message
     *
     * @param msg The parent message.
     */
    async executeRequest(content) {
        const result = await this._remoteKernel.execute(content, this.parent);
        result.execution_count = this.executionCount;
        return result;
    }
    /**
     * Handle an complete_request message
     *
     * @param msg The parent message.
     */
    async completeRequest(content) {
        return await this._remoteKernel.complete(content, this.parent);
    }
    /**
     * Handle an `inspect_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async inspectRequest(content) {
        return await this._remoteKernel.inspect(content, this.parent);
    }
    /**
     * Handle an `is_complete_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async isCompleteRequest(content) {
        return await this._remoteKernel.isComplete(content, this.parent);
    }
    /**
     * Handle a `comm_info_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async commInfoRequest(content) {
        return await this._remoteKernel.commInfo(content, this.parent);
    }
    /**
     * Send an `comm_open` message.
     *
     * @param msg - The comm_open message.
     */
    async commOpen(msg) {
        return await this._remoteKernel.commOpen(msg, this.parent);
    }
    /**
     * Send an `comm_msg` message.
     *
     * @param msg - The comm_msg message.
     */
    async commMsg(msg) {
        return await this._remoteKernel.commMsg(msg, this.parent);
    }
    /**
     * Send an `comm_close` message.
     *
     * @param close - The comm_close message.
     */
    async commClose(msg) {
        return await this._remoteKernel.commClose(msg, this.parent);
    }
    /**
     * Send an `input_reply` message.
     *
     * @param content - The content of the reply.
     */
    async inputReply(content) {
        return await this._remoteKernel.inputReply(content, this.parent);
    }
    _worker;
    _remoteKernel;
    _ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
}


/***/ })

}]);
//# sourceMappingURL=lite_ipykernel_lib_index_js-_d5050.cc00c1aff5f6f6946e11.js.map