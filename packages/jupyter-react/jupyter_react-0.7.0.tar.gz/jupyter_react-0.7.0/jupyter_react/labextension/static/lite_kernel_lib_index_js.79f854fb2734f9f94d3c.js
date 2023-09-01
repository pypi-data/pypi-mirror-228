"use strict";
(self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || []).push([["lite_kernel_lib_index_js"],{

/***/ "../lite/kernel/lib/index.js":
/*!***********************************!*\
  !*** ../lite/kernel/lib/index.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseKernel": () => (/* reexport safe */ _kernel__WEBPACK_IMPORTED_MODULE_0__.BaseKernel),
/* harmony export */   "FALLBACK_KERNEL": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.FALLBACK_KERNEL),
/* harmony export */   "IKernelSpecs": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IKernelSpecs),
/* harmony export */   "IKernels": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IKernels),
/* harmony export */   "KernelSpecs": () => (/* reexport safe */ _kernelspecs__WEBPACK_IMPORTED_MODULE_2__.KernelSpecs),
/* harmony export */   "Kernels": () => (/* reexport safe */ _kernels__WEBPACK_IMPORTED_MODULE_1__.Kernels)
/* harmony export */ });
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./kernel */ "../lite/kernel/lib/kernel.js");
/* harmony import */ var _kernels__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./kernels */ "../lite/kernel/lib/kernels.js");
/* harmony import */ var _kernelspecs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./kernelspecs */ "../lite/kernel/lib/kernelspecs.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../lite/kernel/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/***/ }),

/***/ "../lite/kernel/lib/kernel.js":
/*!************************************!*\
  !*** ../lite/kernel/lib/kernel.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseKernel": () => (/* binding */ BaseKernel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);


/**
 * A base kernel class handling basic kernel messaging.
 */
class BaseKernel {
    /**
     * Construct a new BaseKernel.
     *
     * @param options The instantiation options for a BaseKernel.
     */
    constructor(options) {
        const { id, name, location, sendMessage } = options;
        this._id = id;
        this._name = name;
        this._location = location;
        this._sendMessage = sendMessage;
    }
    /**
     * A promise that is fulfilled when the kernel is ready.
     */
    get ready() {
        return Promise.resolve();
    }
    /**
     * Return whether the kernel is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A signal emitted when the kernel is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Get the kernel id
     */
    get id() {
        return this._id;
    }
    /**
     * Get the name of the kernel
     */
    get name() {
        return this._name;
    }
    /**
     * The location in the virtual filesystem from which the kernel was started.
     */
    get location() {
        return this._location;
    }
    /**
     * The current execution count
     */
    get executionCount() {
        return this._executionCount;
    }
    /**
     * Get the last parent header
     */
    get parentHeader() {
        return this._parentHeader;
    }
    /**
     * Get the last parent message (mimic ipykernel's get_parent)
     */
    get parent() {
        return this._parent;
    }
    /**
     * Dispose the kernel.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit(void 0);
    }
    /**
     * Handle an incoming message from the client.
     *
     * @param msg The message to handle
     */
    async handleMessage(msg) {
        this._busy(msg);
        this._parent = msg;
        const msgType = msg.header.msg_type;
        switch (msgType) {
            case 'kernel_info_request':
                await this._kernelInfo(msg);
                break;
            case 'execute_request':
                await this._execute(msg);
                break;
            case 'input_reply':
                this.inputReply(msg.content);
                break;
            case 'inspect_request':
                await this._inspect(msg);
                break;
            case 'is_complete_request':
                await this._isCompleteRequest(msg);
                break;
            case 'complete_request':
                await this._complete(msg);
                break;
            case 'history_request':
                await this._historyRequest(msg);
                break;
            case 'comm_open':
                await this.commOpen(msg);
                break;
            case 'comm_msg':
                await this.commMsg(msg);
                break;
            case 'comm_close':
                await this.commClose(msg);
                break;
            default:
                break;
        }
        this._idle(msg);
    }
    /**
     * Stream an event from the kernel
     *
     * @param parentHeader The parent header.
     * @param content The stream content.
     */
    stream(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'stream',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `display_data` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The display_data content.
     */
    displayData(content, parentHeader = undefined) {
        // Make sure metadata is always set
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        content.metadata = content.metadata ?? {};
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'display_data',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `input_request` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The input_request content.
     */
    inputRequest(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'stdin',
            msgType: 'input_request',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send an `execute_result` message.
     *
     * @param parentHeader The parent header.
     * @param content The execute result content.
     */
    publishExecuteResult(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'execute_result',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send an `error` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The error content.
     */
    publishExecuteError(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'error',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `update_display_data` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The update_display_data content.
     */
    updateDisplayData(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'update_display_data',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `clear_output` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The clear_output content.
     */
    clearOutput(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'clear_output',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `comm` message to the client.
     *
     * @param .
     */
    handleComm(type, content, metadata, buffers, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: type,
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
            metadata,
            buffers,
        });
        this._sendMessage(message);
    }
    /**
     * Send an 'idle' status message.
     *
     * @param parent The parent message
     */
    _idle(parent) {
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'status',
            session: parent.header.session,
            parentHeader: parent.header,
            channel: 'iopub',
            content: {
                execution_state: 'idle',
            },
        });
        this._sendMessage(message);
    }
    /**
     * Send a 'busy' status message.
     *
     * @param parent The parent message.
     */
    _busy(parent) {
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'status',
            session: parent.header.session,
            parentHeader: parent.header,
            channel: 'iopub',
            content: {
                execution_state: 'busy',
            },
        });
        this._sendMessage(message);
    }
    /**
     * Handle a kernel_info_request message
     *
     * @param parent The parent message.
     */
    async _kernelInfo(parent) {
        const content = await this.kernelInfoRequest();
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'kernel_info_reply',
            channel: 'shell',
            session: parent.header.session,
            parentHeader: parent.header,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle a `history_request` message
     *
     * @param msg The parent message.
     */
    async _historyRequest(msg) {
        const historyMsg = msg;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'history_reply',
            channel: 'shell',
            parentHeader: historyMsg.header,
            session: msg.header.session,
            content: {
                status: 'ok',
                history: this._history,
            },
        });
        this._sendMessage(message);
    }
    /**
     * Send an `execute_input` message.
     *
     * @param msg The parent message.
     */
    _executeInput(msg) {
        const parent = msg;
        const code = parent.content.code;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'execute_input',
            parentHeader: parent.header,
            channel: 'iopub',
            session: msg.header.session,
            content: {
                code,
                execution_count: this._executionCount,
            },
        });
        this._sendMessage(message);
    }
    /**
     * Handle an execute_request message.
     *
     * @param msg The parent message.
     */
    async _execute(msg) {
        const executeMsg = msg;
        const content = executeMsg.content;
        if (content.store_history) {
            this._executionCount++;
        }
        // TODO: handle differently
        this._parentHeader = executeMsg.header;
        this._executeInput(executeMsg);
        if (content.store_history) {
            this._history.push([0, 0, content.code]);
        }
        const reply = await this.executeRequest(executeMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'execute_reply',
            channel: 'shell',
            parentHeader: executeMsg.header,
            session: msg.header.session,
            content: reply,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an complete_request message
     *
     * @param msg The parent message.
     */
    async _complete(msg) {
        const completeMsg = msg;
        const content = await this.completeRequest(completeMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'complete_reply',
            parentHeader: completeMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an inspect_request message
     *
     * @param msg The parent message.
     */
    async _inspect(msg) {
        const inspectMsg = msg;
        const content = await this.inspectRequest(inspectMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'inspect_reply',
            parentHeader: inspectMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an is_complete_request message
     *
     * @param msg The parent message.
     */
    async _isCompleteRequest(msg) {
        const isCompleteMsg = msg;
        const content = await this.isCompleteRequest(isCompleteMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'is_complete_reply',
            parentHeader: isCompleteMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    _id;
    _name;
    _location;
    _history = [];
    _executionCount = 0;
    _isDisposed = false;
    _disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
    _sendMessage;
    _parentHeader = undefined;
    _parent = undefined;
}


/***/ }),

/***/ "../lite/kernel/lib/kernels.js":
/*!*************************************!*\
  !*** ../lite/kernel/lib/kernels.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Kernels": () => (/* binding */ Kernels)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services/lib/kernel/serialize */ "../../../../../node_modules/@jupyterlab/services/lib/kernel/serialize.js");
/* harmony import */ var _jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var mock_socket__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! mock-socket */ "../../../../../node_modules/mock-socket/dist/mock-socket.js");
/* harmony import */ var mock_socket__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(mock_socket__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var async_mutex__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! async-mutex */ "../../../../../node_modules/async-mutex/index.mjs");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);






/**
 * A class to handle requests to /api/kernels
 */
class Kernels {
    /**
     * Construct a new Kernels
     *
     * @param options The instantiation options
     */
    constructor(options) {
        const { kernelspecs } = options;
        this._kernelspecs = kernelspecs;
    }
    /**
     * Start a new kernel.
     *
     * @param options The kernel start options.
     */
    async startNew(options) {
        const { id, name, location } = options;
        const factory = this._kernelspecs.factories.get(name);
        // bail if there is no factory associated with the requested kernel
        if (!factory) {
            return { id, name };
        }
        // create a synchronization mechanism to allow only one message
        // to be processed at a time
        const mutex = new async_mutex__WEBPACK_IMPORTED_MODULE_4__.Mutex();
        // hook a new client to a kernel
        const hook = (kernelId, clientId, socket) => {
            const kernel = this._kernels.get(kernelId);
            if (!kernel) {
                throw Error(`No kernel ${kernelId}`);
            }
            this._clients.set(clientId, socket);
            this._kernelClients.get(kernelId)?.add(clientId);
            const processMsg = async (msg) => {
                await mutex.runExclusive(async () => {
                    await kernel.handleMessage(msg);
                });
            };
            socket.on('message', async (message) => {
                let msg;
                if (message instanceof ArrayBuffer) {
                    message = new Uint8Array(message).buffer;
                    msg = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.deserialize)(message, 'v1.kernel.websocket.jupyter.org');
                }
                else if (typeof message === 'string') {
                    const enc = new TextEncoder();
                    const mb = enc.encode(message);
                    msg = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.deserialize)(mb, 'v1.kernel.websocket.jupyter.org');
                }
                else {
                    return;
                }
                // TODO Find a better solution for this?
                // input-reply is asynchronous, must not be processed like other messages
                if (msg.header.msg_type === 'input_reply') {
                    kernel.handleMessage(msg);
                }
                else {
                    void processMsg(msg);
                }
            });
            const removeClient = () => {
                this._clients.delete(clientId);
                this._kernelClients.get(kernelId)?.delete(clientId);
            };
            kernel.disposed.connect(removeClient);
            // TODO: check whether this is called
            // https://github.com/thoov/mock-socket/issues/298
            // https://github.com/jupyterlab/jupyterlab/blob/6bc884a7a8ed73c615ce72ba097bdb790482b5bf/packages/services/src/kernel/default.ts#L1245
            socket.onclose = removeClient;
        };
        // ensure kernel id
        const kernelId = id ?? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4();
        // There is one server per kernel which handles multiple clients
        const kernelUrl = `${Kernels.WS_BASE_URL}api/kernels/${kernelId}/channels`;
        const runningKernel = this._kernels.get(kernelId);
        if (runningKernel) {
            return {
                id: runningKernel.id,
                name: runningKernel.name,
            };
        }
        // start the kernel
        const sendMessage = (msg) => {
            const clientId = msg.header.session;
            const socket = this._clients.get(clientId);
            if (!socket) {
                console.warn(`Trying to send message on removed socket for kernel ${kernelId}`);
                return;
            }
            const message = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.serialize)(msg, 'v1.kernel.websocket.jupyter.org');
            // process iopub messages
            if (msg.channel === 'iopub') {
                const clients = this._kernelClients.get(kernelId);
                clients?.forEach((id) => {
                    this._clients.get(id)?.send(message);
                });
                return;
            }
            socket.send(message);
        };
        const kernel = await factory({
            id: kernelId,
            sendMessage,
            name,
            location,
        });
        await kernel.ready;
        this._kernels.set(kernelId, kernel);
        this._kernelClients.set(kernelId, new Set());
        // create the websocket server for the kernel
        const wsServer = new mock_socket__WEBPACK_IMPORTED_MODULE_3__.Server(kernelUrl);
        wsServer.on('connection', (socket) => {
            const url = new URL(socket.url);
            const clientId = url.searchParams.get('session_id') ?? '';
            hook(kernelId, clientId, socket);
        });
        // clean up closed connection
        wsServer.on('close', () => {
            this._clients.keys().forEach((clientId) => {
                const socket = this._clients.get(clientId);
                if (socket?.readyState === WebSocket.CLOSED) {
                    this._clients.delete(clientId);
                    this._kernelClients.get(kernelId)?.delete(clientId);
                }
            });
        });
        // cleanup on kernel shutdown
        kernel.disposed.connect(() => {
            wsServer.close();
            this._kernels.delete(kernelId);
            this._kernelClients.delete(kernelId);
        });
        return {
            id: kernel.id,
            name: kernel.name,
        };
    }
    /**
     * Restart a kernel.
     *
     * @param kernelId The kernel id.
     */
    async restart(kernelId) {
        const kernel = this._kernels.get(kernelId);
        if (!kernel) {
            throw Error(`Kernel ${kernelId} does not exist`);
        }
        const { id, name, location } = kernel;
        kernel.dispose();
        return this.startNew({ id, name, location });
    }
    /**
     * Shut down a kernel.
     *
     * @param id The kernel id.
     */
    async shutdown(id) {
        this._kernels.delete(id)?.dispose();
    }
    _kernels = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _clients = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _kernelClients = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _kernelspecs;
}
/**
 * A namespace for Kernels statics.
 */
(function (Kernels) {
    /**
     * The base url for the Kernels manager
     */
    Kernels.WS_BASE_URL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PageConfig.getBaseUrl().replace(/^http/, 'ws');
})(Kernels || (Kernels = {}));


/***/ }),

/***/ "../lite/kernel/lib/kernelspecs.js":
/*!*****************************************!*\
  !*** ../lite/kernel/lib/kernelspecs.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelSpecs": () => (/* binding */ KernelSpecs)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../lite/kernel/lib/tokens.js");


/**
 * A class to handle requests to /api/kernelspecs
 */
class KernelSpecs {
    /**
     * Get the kernel specs.
     */
    get specs() {
        if (this._specs.size === 0) {
            return null;
        }
        return {
            default: this.defaultKernelName,
            kernelspecs: Object.fromEntries(this._specs),
        };
    }
    /**
     * Get the default kernel name.
     */
    get defaultKernelName() {
        let defaultKernelName = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('defaultKernelName');
        if (!defaultKernelName && this._specs.size) {
            const keys = Array.from(this._specs.keys());
            keys.sort();
            defaultKernelName = keys[0];
        }
        return defaultKernelName || _tokens__WEBPACK_IMPORTED_MODULE_1__.FALLBACK_KERNEL;
    }
    /**
     * Get the kernel factories for the current kernels.
     */
    get factories() {
        return this._factories;
    }
    /**
     * Register a new kernel.
     *
     * @param options The options to register a new kernel.
     */
    register(options) {
        const { spec, create } = options;
        this._specs.set(spec.name, spec);
        this._factories.set(spec.name, create);
    }
    _specs = new Map();
    _factories = new Map();
}


/***/ }),

/***/ "../lite/kernel/lib/tokens.js":
/*!************************************!*\
  !*** ../lite/kernel/lib/tokens.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FALLBACK_KERNEL": () => (/* binding */ FALLBACK_KERNEL),
/* harmony export */   "IKernelSpecs": () => (/* binding */ IKernelSpecs),
/* harmony export */   "IKernels": () => (/* binding */ IKernels)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The token for the kernels service.
 */
const IKernels = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-kernel:IKernels');
/**
 * The kernel name of last resort.
 */
const FALLBACK_KERNEL = 'javascript';
/**
 * The token for the kernel spec service.
 */
const IKernelSpecs = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-kernel:IKernelSpecs');


/***/ })

}]);
//# sourceMappingURL=lite_kernel_lib_index_js.79f854fb2734f9f94d3c.js.map