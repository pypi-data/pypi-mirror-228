var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/@datalayer/jupyter-react":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base-manager_lib_index_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_css_widgets-base_css"), __webpack_require__.e("vendors-node_modules_primer_react_lib-esm_ActionList_index_js-node_modules_primer_react_lib-e-b0bc35"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_lib_services-shim_js-node_modules_jupyter-widgets_c-602195"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_output_jupyter-widgets_output-webpack_sharing-ed5f68"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_state-webpack_sharing_consume_default_codemirror_view"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base-manager_lib_index_js"), __webpack_require__.e("vendors-node_modules_primer_react_lib-esm_ActionList_index_js-node_modules_primer_react_lib-e-b0bc35"), __webpack_require__.e("vendors-node_modules_jupyterlab_ui-components_lib_icon_labicon_js-node_modules_primer_react_l-ca6b63"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0"), __webpack_require__.e("lib_jupyter_lab_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/jupyter/lab/index.js */ "./lib/jupyter/lab/index.js")))));
	},
	"./style": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("style_index_js")]).then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/create fake namespace object */
/******/ 	(() => {
/******/ 		var getProto = Object.getPrototypeOf ? (obj) => (Object.getPrototypeOf(obj)) : (obj) => (obj.__proto__);
/******/ 		var leafPrototypes;
/******/ 		// create a fake namespace object
/******/ 		// mode & 1: value is a module id, require it
/******/ 		// mode & 2: merge all properties of value into the ns
/******/ 		// mode & 4: return value when already ns object
/******/ 		// mode & 16: return value when it's Promise-like
/******/ 		// mode & 8|1: behave like require
/******/ 		__webpack_require__.t = function(value, mode) {
/******/ 			if(mode & 1) value = this(value);
/******/ 			if(mode & 8) return value;
/******/ 			if(typeof value === 'object' && value) {
/******/ 				if((mode & 4) && value.__esModule) return value;
/******/ 				if((mode & 16) && typeof value.then === 'function') return value;
/******/ 			}
/******/ 			var ns = Object.create(null);
/******/ 			__webpack_require__.r(ns);
/******/ 			var def = {};
/******/ 			leafPrototypes = leafPrototypes || [null, getProto({}), getProto([]), getProto(getProto)];
/******/ 			for(var current = mode & 2 && value; typeof current == 'object' && !~leafPrototypes.indexOf(current); current = getProto(current)) {
/******/ 				Object.getOwnPropertyNames(current).forEach((key) => (def[key] = () => (value[key])));
/******/ 			}
/******/ 			def['default'] = () => (value);
/******/ 			__webpack_require__.d(ns, def);
/******/ 			return ns;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_jquery_dist_jquery_js":"54fcba85b858f83893bf","vendors-node_modules_rxjs__esm5_internal_operators_map_js":"8ddd7b922d3dcdea6c24","vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1":"f5938d4c933bb6114315","vendors-node_modules_jupyter-widgets_base-manager_lib_index_js":"d62b51fd839526a75e1b","vendors-node_modules_jupyter-widgets_controls_css_widgets-base_css":"85413c5be384c392eeea","vendors-node_modules_primer_react_lib-esm_ActionList_index_js-node_modules_primer_react_lib-e-b0bc35":"7b49dc7839078230dc1c","vendors-node_modules_jupyter-widgets_base_lib_services-shim_js-node_modules_jupyter-widgets_c-602195":"67bfbb399e54ecd5e56d","webpack_sharing_consume_default_lumino_coreutils":"418a1cf9639409920699","webpack_sharing_consume_default_lumino_signaling":"38729667cd73aa094405","webpack_sharing_consume_default_lumino_messaging":"a57f8b6b22be9b070dc3","webpack_sharing_consume_default_jupyterlab_coreutils":"8d78a44f7f2846bef732","webpack_sharing_consume_default_react":"f7ebfecf762709b0381f","webpack_sharing_consume_default_lumino_widgets":"aafc9cd2ebeb7ac533fe","webpack_sharing_consume_default_lumino_algorithm":"c0c89468bd1e543c047d","webpack_sharing_consume_default_jupyterlab_services":"fdc07f97fde21b7bf746","webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base":"c918ed21df5601c8d14f","webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server":"4b1be6fbc5bf87140fb8","webpack_sharing_consume_default_react-dom":"af1489e6d9e2d77eb49e","lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0":"08c75cdca7e73b05f04c","webpack_sharing_consume_default_jupyter-widgets_output_jupyter-widgets_output-webpack_sharing-ed5f68":"d5aa42cc52429793f012","webpack_sharing_consume_default_codemirror_state-webpack_sharing_consume_default_codemirror_view":"9fdbb6cb817522928f5a","lib_index_js":"51412c01f69ec0297f68","vendors-node_modules_jupyterlab_ui-components_lib_icon_labicon_js-node_modules_primer_react_l-ca6b63":"f58d03d26d013b9fd3c9","lib_jupyter_lab_index_js":"2ad407681386fad9f5cf","style_index_js":"74eef6f0da21b5a376c8","vendors-node_modules_lezer_lr_dist_index_js":"e66c8130d2ea928c8be8","vendors-node_modules_codemirror_lang-python_dist_index_js":"2fc0ad931709e62d6a5c","webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common":"48ffebfac3c877e9b702","webpack_sharing_consume_default_lezer_highlight":"886d90ad41ead9553783","node_modules_process_browser_js-_4e960":"3511a473f2a0a7cb0fe6","webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel":"c6f5b709bf78bb9568c7","lite_ipykernel-extension_lib_index_js-_67640":"3979ebb100afdcc1993e","vendors-node_modules_comlink_dist_esm_comlink_mjs":"c52f9c04c1757e043986","lite_ipykernel_lib_worker_js":"04fbee896cb193d87636","lite_ipykernel_lib_index_js-_d5050":"cc00c1aff5f6f6946e11","vendors-node_modules_mock-socket_dist_mock-socket_js":"535a9007ba04518fd091","vendors-node_modules_async-mutex_index_mjs-node_modules_jupyterlab_services_lib_kernel_serialize_js":"556dea66ad26f2b2e827","lite_kernel_lib_index_js":"79f854fb2734f9f94d3c","vendors-node_modules_json5_dist_index_js-node_modules_localforage_dist_localforage_js":"5d4bc2061b33c83f344c","lite_server-extension_lib_index_js":"81d7f52536a267f416e7","lite_server_lib_index_js":"8c2d7776246dea6d9b4a","vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732":"828dba19d093b12ef2ea","vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852":"9b28debaf804ba0e5841","vendors-node_modules_datalayer_typescript-fsa-redux-observable_lib_index_js":"cc753630fa55de280344","node_modules_rxjs__esm5_internal_operators_ignoreElements_js-node_modules_rxjs__esm5_internal-39ebda":"8aaece873db64d43dcda","vendors-node_modules_jupyter-widgets_base_lib_index_js":"8f8e815c4e63bf3681a4","vendors-node_modules_jupyter-widgets_controls_lib_index_js":"b853aaf1fb743ebee8e9","webpack_sharing_consume_default_lumino_domutils":"8206c25bb7514ecf78c3","vendors-node_modules_css-loader_dist_runtime_getUrl_js-node_modules_lumino_widgets_style_index_css":"3c22ec14f1a6220c6511","vendors-node_modules_jupyter-widgets_html-manager_lib_index_js":"3b6a801dec457547837b","webpack_sharing_consume_default_jupyter-widgets_controls_jupyter-widgets_controls":"7f977d3fdead0fb7d966","node_modules_jupyter-widgets_html-manager_lib_output_renderers_js":"ae370e9ef77165632557","node_modules_jupyter-widgets_output_lib_index_js-_c56a0":"a824220b9652d379d05e","vendors-node_modules_codemirror_autocomplete_dist_index_js":"ec2b2890d4b91b71fe5d","vendors-node_modules_codemirror_dist_index_js":"946b553eb89f9c627525","vendors-node_modules_marked_lib_marked_esm_js":"e9d62f96e7af38fe9e6f","node_modules_react-error-boundary_dist_react-error-boundary_umd_js-_4c630":"d27a6d6d1966032c6c3b","vendors-node_modules_react-redux_es_index_js":"893bacf4746186bf1b58","node_modules_object-assign_index_js":"74fcd742e3352a8cbbc8","vendors-node_modules_redux-observable_lib_esm_index_js":"354c634040cdf4c490e5","webpack_sharing_consume_default_rxjs_rxjs":"c681c2a6336b45f98938","vendors-node_modules_redux_es_redux_js":"d6649797eb748d84cb22","vendors-node_modules_rxjs__esm5_index_js":"ad8256eb9a46a8bdc71b","node_modules_rxjs__esm5_internal_util_noop_js-_6c8c0":"90d3eedeb243c544fa18","vendors-node_modules_styled-components_dist_styled-components_browser_esm_js":"e83a20dab9ebd4d57861","node_modules_process_browser_js-_4e961":"9bfe8cf3fbcf7bb4b569","node_modules_typescript-fsa-reducers_dist_index_js":"1072374f09474598fc6f","node_modules_typescript-fsa_lib_index_js":"f8e4989847a465344dc8","vendors-node_modules_jupyter-widgets_base_css_index_css-node_modules_jupyterlab_apputils_styl-92be6d":"144d453a1f2fda9a8ad0","lib_jupyter_lab_JupyterLabCss_js":"8b31178c76c09825a764","node_modules_react-error-boundary_dist_react-error-boundary_umd_js-_4c631":"092ba3994ea1492af840","webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel-extension_datalayer_jupyterli-4c7967":"30643bebcf47121bfc74","webpack_sharing_consume_default_datalayer_jupyterlite-server-extension_datalayer_jupyterlite--eaaa26":"7ca8fc2adbcf2e1e9258","vendors-node_modules_codemirror_lang-markdown_dist_index_js":"45a9964e2a00e2f8f5ae","node_modules_jupyter-widgets_output_lib_index_js-_c56a1":"278b80afcca40c237692","webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel_datalayer_jupyterlite-ipykernel":"b2dcc910ec456eda8bb2","node_modules_rxjs__esm5_internal_util_noop_js-_6c8c1":"fcf4df12bc2416c0687d","lite_ipykernel-extension_lib_index_js-_67641":"d8411a5817ebf045633f","lite_ipykernel_lib_index_js-_d5051":"59fdcb8d1a9791741103","lite_ipykernel_lib_comlink_worker_js":"108ebc3ba258adcdd784"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "@datalayer/jupyter-react:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/node module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.nmd = (module) => {
/******/ 			module.paths = [];
/******/ 			if (!module.children) module.children = [];
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "@datalayer/jupyter-react";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@codemirror/lang-python", "6.0.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("webpack_sharing_consume_default_lezer_highlight"), __webpack_require__.e("node_modules_process_browser_js-_4e960")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@codemirror/lang-python/dist/index.js */ "../../../../../node_modules/@codemirror/lang-python/dist/index.js"))))));
/******/ 					register("@datalayer/jupyter-react", "0.7.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base-manager_lib_index_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_css_widgets-base_css"), __webpack_require__.e("vendors-node_modules_primer_react_lib-esm_ActionList_index_js-node_modules_primer_react_lib-e-b0bc35"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_lib_services-shim_js-node_modules_jupyter-widgets_c-602195"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_output_jupyter-widgets_output-webpack_sharing-ed5f68"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_state-webpack_sharing_consume_default_codemirror_view"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("@datalayer/jupyterlite-ipykernel-extension", "0.1.0-beta.13", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server"), __webpack_require__.e("lite_ipykernel-extension_lib_index_js-_67640")]).then(() => (() => (__webpack_require__(/*! ../lite/ipykernel-extension/lib/index.js */ "../lite/ipykernel-extension/lib/index.js"))))));
/******/ 					register("@datalayer/jupyterlite-ipykernel", "0.1.0-beta.13", () => (Promise.all([__webpack_require__.e("vendors-node_modules_comlink_dist_esm_comlink_mjs"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel"), __webpack_require__.e("lite_ipykernel_lib_worker_js"), __webpack_require__.e("lite_ipykernel_lib_index_js-_d5050")]).then(() => (() => (__webpack_require__(/*! ../lite/ipykernel/lib/index.js */ "../lite/ipykernel/lib/index.js"))))));
/******/ 					register("@datalayer/jupyterlite-kernel", "0.1.0-beta.13", () => (Promise.all([__webpack_require__.e("vendors-node_modules_mock-socket_dist_mock-socket_js"), __webpack_require__.e("vendors-node_modules_async-mutex_index_mjs-node_modules_jupyterlab_services_lib_kernel_serialize_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("lite_kernel_lib_index_js")]).then(() => (() => (__webpack_require__(/*! ../lite/kernel/lib/index.js */ "../lite/kernel/lib/index.js"))))));
/******/ 					register("@datalayer/jupyterlite-server-extension", "0.1.0-beta.13", () => (Promise.all([__webpack_require__.e("vendors-node_modules_json5_dist_index_js-node_modules_localforage_dist_localforage_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server"), __webpack_require__.e("lite_server-extension_lib_index_js")]).then(() => (() => (__webpack_require__(/*! ../lite/server-extension/lib/index.js */ "../lite/server-extension/lib/index.js"))))));
/******/ 					register("@datalayer/jupyterlite-server", "0.1.0-beta.13", () => (Promise.all([__webpack_require__.e("vendors-node_modules_mock-socket_dist_mock-socket_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("lite_server_lib_index_js")]).then(() => (() => (__webpack_require__(/*! ../lite/server/lib/index.js */ "../lite/server/lib/index.js"))))));
/******/ 					register("@datalayer/typescript-fsa-redux-observable", "0.18.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_datalayer_typescript-fsa-redux-observable_lib_index_js"), __webpack_require__.e("node_modules_rxjs__esm5_internal_operators_ignoreElements_js-node_modules_rxjs__esm5_internal-39ebda")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@datalayer/typescript-fsa-redux-observable/lib/index.js */ "../../../../../node_modules/@datalayer/typescript-fsa-redux-observable/lib/index.js"))))));
/******/ 					register("@jupyter-widgets/base", "6.0.5", () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@jupyter-widgets/base/lib/index.js */ "../../../../../node_modules/@jupyter-widgets/base/lib/index.js"))))));
/******/ 					register("@jupyter-widgets/controls", "5.0.6", () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("webpack_sharing_consume_default_lumino_domutils")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@jupyter-widgets/controls/lib/index.js */ "../../../../../node_modules/@jupyter-widgets/controls/lib/index.js"))))));
/******/ 					register("@jupyter-widgets/html-manager", "1.0.8", () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base-manager_lib_index_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_css_widgets-base_css"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_getUrl_js-node_modules_lumino_widgets_style_index_css"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_html-manager_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_output_jupyter-widgets_output-webpack_sharing-ed5f68"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_controls_jupyter-widgets_controls"), __webpack_require__.e("node_modules_jupyter-widgets_html-manager_lib_output_renderers_js")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@jupyter-widgets/html-manager/lib/index.js */ "../../../../../node_modules/@jupyter-widgets/html-manager/lib/index.js"))))));
/******/ 					register("@jupyter-widgets/output", "6.0.5", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base"), __webpack_require__.e("node_modules_jupyter-widgets_output_lib_index_js-_c56a0")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/@jupyter-widgets/output/lib/index.js */ "../../../../../node_modules/@jupyter-widgets/output/lib/index.js"))))));
/******/ 					register("codemirror", "6.0.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_state-webpack_sharing_consume_default_codemirror_view")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/codemirror/dist/index.js */ "../../../../../node_modules/codemirror/dist/index.js"))))));
/******/ 					register("marked", "4.0.10", () => (__webpack_require__.e("vendors-node_modules_marked_lib_marked_esm_js").then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/marked/lib/marked.esm.js */ "../../../../../node_modules/marked/lib/marked.esm.js"))))));
/******/ 					register("react-error-boundary", "3.1.3", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_react-error-boundary_dist_react-error-boundary_umd_js-_4c630")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/react-error-boundary/dist/react-error-boundary.umd.js */ "../../../../../node_modules/react-error-boundary/dist/react-error-boundary.umd.js"))))));
/******/ 					register("react-redux", "7.2.4", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react-redux_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("node_modules_object-assign_index_js")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/react-redux/es/index.js */ "../../../../../node_modules/react-redux/es/index.js"))))));
/******/ 					register("redux-observable", "1.2.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_redux-observable_lib_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_rxjs_rxjs")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/redux-observable/lib/esm/index.js */ "../../../../../node_modules/redux-observable/lib/esm/index.js"))))));
/******/ 					register("redux", "4.1.0", () => (__webpack_require__.e("vendors-node_modules_redux_es_redux_js").then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/redux/es/redux.js */ "../../../../../node_modules/redux/es/redux.js"))))));
/******/ 					register("rxjs", "6.6.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_index_js"), __webpack_require__.e("node_modules_rxjs__esm5_internal_util_noop_js-_6c8c0")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/rxjs/_esm5/index.js */ "../../../../../node_modules/rxjs/_esm5/index.js"))))));
/******/ 					register("styled-components", "5.3.10", () => (Promise.all([__webpack_require__.e("vendors-node_modules_styled-components_dist_styled-components_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_process_browser_js-_4e961")]).then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/styled-components/dist/styled-components.browser.esm.js */ "../../../../../node_modules/styled-components/dist/styled-components.browser.esm.js"))))));
/******/ 					register("typescript-fsa-reducers", "1.2.1", () => (__webpack_require__.e("node_modules_typescript-fsa-reducers_dist_index_js").then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/typescript-fsa-reducers/dist/index.js */ "../../../../../node_modules/typescript-fsa-reducers/dist/index.js"))))));
/******/ 					register("typescript-fsa", "3.0.0", () => (__webpack_require__.e("node_modules_typescript-fsa_lib_index_js").then(() => (() => (__webpack_require__(/*! ../../../../../node_modules/typescript-fsa/lib/index.js */ "../../../../../node_modules/typescript-fsa/lib/index.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": () => (loadSingletonVersionCheck("default", "@lumino/coreutils", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/signaling": () => (loadSingletonVersionCheck("default", "@lumino/signaling", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/messaging": () => (loadSingletonVersionCheck("default", "@lumino/messaging", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/coreutils": () => (loadSingletonVersionCheck("default", "@jupyterlab/coreutils", [1,6,0,3])),
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/widgets": () => (loadSingletonVersionCheck("default", "@lumino/widgets", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@lumino/algorithm": () => (loadSingletonVersionCheck("default", "@lumino/algorithm", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersionCheck("default", "@jupyterlab/services", [1,7,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base?a94e": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/base", [1,6,0,5], () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_widgets")]).then(() => (() => (__webpack_require__(/*! @jupyter-widgets/base */ "../../../../../node_modules/@jupyter-widgets/base/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyterlite-server/@datalayer/jupyterlite-server": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyterlite-server", [7,0,1,0,,"beta",13], () => (Promise.all([__webpack_require__.e("vendors-node_modules_mock-socket_dist_mock-socket_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("lite_server_lib_index_js")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyterlite-server */ "../lite/server/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersionCheck("default", "react-dom", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,4,1,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": () => (loadSingletonVersionCheck("default", "@jupyterlab/notebook", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base?5ccc": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/base", [4,6,0,5], () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_base_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging")]).then(() => (() => (__webpack_require__(/*! @jupyter-widgets/base */ "../../../../../node_modules/@jupyter-widgets/base/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls?27d1": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/controls", [4,5,0,6], () => (Promise.all([__webpack_require__.e("vendors-node_modules_jquery_dist_jquery_js"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_messaging"), __webpack_require__.e("webpack_sharing_consume_default_lumino_domutils")]).then(() => (() => (__webpack_require__(/*! @jupyter-widgets/controls */ "../../../../../node_modules/@jupyter-widgets/controls/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-error-boundary/react-error-boundary": () => (loadStrictVersionCheckFallback("default", "react-error-boundary", [4,3,1,3], () => (__webpack_require__.e("node_modules_react-error-boundary_dist_react-error-boundary_umd_js-_4c631").then(() => (() => (__webpack_require__(/*! react-error-boundary */ "../../../../../node_modules/react-error-boundary/dist/react-error-boundary.umd.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-redux/react-redux": () => (loadStrictVersionCheckFallback("default", "react-redux", [4,7,2,4], () => (__webpack_require__.e("vendors-node_modules_react-redux_es_index_js").then(() => (() => (__webpack_require__(/*! react-redux */ "../../../../../node_modules/react-redux/es/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/redux/redux": () => (loadStrictVersionCheckFallback("default", "redux", [4,4,0,5], () => (__webpack_require__.e("vendors-node_modules_redux_es_redux_js").then(() => (() => (__webpack_require__(/*! redux */ "../../../../../node_modules/redux/es/redux.js"))))))),
/******/ 			"webpack/sharing/consume/default/typescript-fsa/typescript-fsa": () => (loadStrictVersionCheckFallback("default", "typescript-fsa", [4,3,0,0], () => (__webpack_require__.e("node_modules_typescript-fsa_lib_index_js").then(() => (() => (__webpack_require__(/*! typescript-fsa */ "../../../../../node_modules/typescript-fsa/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/typescript-fsa-reducers/typescript-fsa-reducers": () => (loadStrictVersionCheckFallback("default", "typescript-fsa-reducers", [4,1,2,1], () => (__webpack_require__.e("node_modules_typescript-fsa-reducers_dist_index_js").then(() => (() => (__webpack_require__(/*! typescript-fsa-reducers */ "../../../../../node_modules/typescript-fsa-reducers/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/redux-observable/redux-observable": () => (loadStrictVersionCheckFallback("default", "redux-observable", [4,1,2,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_map_js"), __webpack_require__.e("vendors-node_modules_redux-observable_lib_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_rxjs_rxjs")]).then(() => (() => (__webpack_require__(/*! redux-observable */ "../../../../../node_modules/redux-observable/lib/esm/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/styled-components/styled-components": () => (loadStrictVersionCheckFallback("default", "styled-components", [1,5], () => (__webpack_require__.e("vendors-node_modules_styled-components_dist_styled-components_browser_esm_js").then(() => (() => (__webpack_require__(/*! styled-components */ "../../../../../node_modules/styled-components/dist/styled-components.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": () => (loadSingletonVersionCheck("default", "@jupyterlab/rendermime", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/outputarea": () => (loadVersionCheck("default", "@jupyterlab/outputarea", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/output/@jupyter-widgets/output?56a9": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/output", [1,6,0,5], () => (__webpack_require__.e("node_modules_jupyter-widgets_output_lib_index_js-_c56a1").then(() => (() => (__webpack_require__(/*! @jupyter-widgets/output */ "../../../../../node_modules/@jupyter-widgets/output/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/view": () => (loadSingletonVersionCheck("default", "@codemirror/view", [1,6,9,6])),
/******/ 			"webpack/sharing/consume/default/@codemirror/state": () => (loadSingletonVersionCheck("default", "@codemirror/state", [1,6,2,0])),
/******/ 			"webpack/sharing/consume/default/rxjs/rxjs?f93d": () => (loadStrictVersionCheckFallback("default", "rxjs", [4,6,6,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_index_js")]).then(() => (() => (__webpack_require__(/*! rxjs */ "../../../../../node_modules/rxjs/_esm5/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/typescript-fsa-redux-observable/@datalayer/typescript-fsa-redux-observable": () => (loadStrictVersionCheckFallback("default", "@datalayer/typescript-fsa-redux-observable", [4,0,18,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_operators_filter_js-node_modules_rxjs__esm5_internal-288852"), __webpack_require__.e("vendors-node_modules_datalayer_typescript-fsa-redux-observable_lib_index_js")]).then(() => (() => (__webpack_require__(/*! @datalayer/typescript-fsa-redux-observable */ "../../../../../node_modules/@datalayer/typescript-fsa-redux-observable/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/documentsearch": () => (loadSingletonVersionCheck("default", "@jupyterlab/documentsearch", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/translation": () => (loadSingletonVersionCheck("default", "@jupyterlab/translation", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/cells": () => (loadVersionCheck("default", "@jupyterlab/cells", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@lumino/commands": () => (loadSingletonVersionCheck("default", "@lumino/commands", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/codemirror": () => (loadSingletonVersionCheck("default", "@jupyterlab/codemirror", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/completer": () => (loadSingletonVersionCheck("default", "@jupyterlab/completer", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": () => (loadSingletonVersionCheck("default", "@jupyterlab/ui-components", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyter/ydoc": () => (loadSingletonVersionCheck("default", "@jupyter/ydoc", [1,1,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/html-manager/@jupyter-widgets/html-manager": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/html-manager", [4,1,0,8], () => (Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_getUrl_js-node_modules_lumino_widgets_style_index_css"), __webpack_require__.e("vendors-node_modules_jupyter-widgets_html-manager_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_controls_jupyter-widgets_controls")]).then(() => (() => (__webpack_require__(/*! @jupyter-widgets/html-manager */ "../../../../../node_modules/@jupyter-widgets/html-manager/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/codemirror/codemirror": () => (loadStrictVersionCheckFallback("default", "codemirror", [4,6,0,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_codemirror_autocomplete_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common")]).then(() => (() => (__webpack_require__(/*! codemirror */ "../../../../../node_modules/codemirror/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@codemirror/lang-python/@codemirror/lang-python": () => (loadStrictVersionCheckFallback("default", "@codemirror/lang-python", [4,6,0,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_lezer_lr_dist_index_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common"), __webpack_require__.e("webpack_sharing_consume_default_lezer_highlight")]).then(() => (() => (__webpack_require__(/*! @codemirror/lang-python */ "../../../../../node_modules/@codemirror/lang-python/dist/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docregistry": () => (loadVersionCheck("default", "@jupyterlab/docregistry", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/json-extension": () => (loadVersionCheck("default", "@jupyterlab/json-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/javascript-extension": () => (loadVersionCheck("default", "@jupyterlab/javascript-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/mathjax-extension": () => (loadVersionCheck("default", "@jupyterlab/mathjax-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/marked/marked": () => (loadStrictVersionCheckFallback("default", "marked", [4,4,0,10], () => (__webpack_require__.e("vendors-node_modules_marked_lib_marked_esm_js").then(() => (() => (__webpack_require__(/*! marked */ "../../../../../node_modules/marked/lib/marked.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@lumino/disposable": () => (loadSingletonVersionCheck("default", "@lumino/disposable", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/properties": () => (loadSingletonVersionCheck("default", "@lumino/properties", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/output/@jupyter-widgets/output?aa08": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/output", [4,6,0,5], () => (__webpack_require__.e("node_modules_jupyter-widgets_output_lib_index_js-_c56a1").then(() => (() => (__webpack_require__(/*! @jupyter-widgets/output */ "../../../../../node_modules/@jupyter-widgets/output/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/console": () => (loadSingletonVersionCheck("default", "@jupyterlab/console", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docmanager": () => (loadSingletonVersionCheck("default", "@jupyterlab/docmanager", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/filebrowser": () => (loadSingletonVersionCheck("default", "@jupyterlab/filebrowser", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/fileeditor": () => (loadSingletonVersionCheck("default", "@jupyterlab/fileeditor", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/terminal": () => (loadSingletonVersionCheck("default", "@jupyterlab/terminal", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/settingregistry": () => (loadSingletonVersionCheck("default", "@jupyterlab/settingregistry", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/launcher": () => (loadSingletonVersionCheck("default", "@jupyterlab/launcher", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/codeeditor": () => (loadSingletonVersionCheck("default", "@jupyterlab/codeeditor", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@codemirror/language": () => (loadSingletonVersionCheck("default", "@codemirror/language", [1,6,0,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/common": () => (loadSingletonVersionCheck("default", "@lezer/common", [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/highlight": () => (loadSingletonVersionCheck("default", "@lezer/highlight", [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyterlite-kernel/@datalayer/jupyterlite-kernel": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyterlite-kernel", [7,0,1,0,,"beta",13], () => (Promise.all([__webpack_require__.e("vendors-node_modules_mock-socket_dist_mock-socket_js"), __webpack_require__.e("vendors-node_modules_async-mutex_index_mjs-node_modules_jupyterlab_services_lib_kernel_serialize_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_services"), __webpack_require__.e("lite_kernel_lib_index_js")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../lite/kernel/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/observables": () => (loadVersionCheck("default", "@jupyterlab/observables", [1,5,0,3])),
/******/ 			"webpack/sharing/consume/default/@lumino/application": () => (loadSingletonVersionCheck("default", "@lumino/application", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@lumino/domutils": () => (loadSingletonVersionCheck("default", "@lumino/domutils", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls?13a6": () => (loadStrictVersionCheckFallback("default", "@jupyter-widgets/controls", [1,5,0,6], () => (Promise.all([__webpack_require__.e("vendors-node_modules_jupyter-widgets_controls_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_lumino_signaling"), __webpack_require__.e("webpack_sharing_consume_default_lumino_algorithm"), __webpack_require__.e("webpack_sharing_consume_default_lumino_domutils")]).then(() => (() => (__webpack_require__(/*! @jupyter-widgets/controls */ "../../../../../node_modules/@jupyter-widgets/controls/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/rxjs/rxjs?4a1c": () => (loadStrictVersionCheckFallback("default", "rxjs", [,[-1,7],[0,6,0,0,,"beta",0],2], () => (Promise.all([__webpack_require__.e("vendors-node_modules_rxjs__esm5_internal_AsyncSubject_js-node_modules_rxjs__esm5_internal_Beh-f72732"), __webpack_require__.e("vendors-node_modules_rxjs__esm5_index_js"), __webpack_require__.e("node_modules_rxjs__esm5_internal_util_noop_js-_6c8c1")]).then(() => (() => (__webpack_require__(/*! rxjs */ "../../../../../node_modules/rxjs/_esm5/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel-extension/@datalayer/jupyterlite-ipykernel-extension": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyterlite-ipykernel-extension", [7,0,1,0,,"beta",13], () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel"), __webpack_require__.e("lite_ipykernel-extension_lib_index_js-_67641")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyterlite-ipykernel-extension */ "../lite/ipykernel-extension/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyterlite-server-extension/@datalayer/jupyterlite-server-extension": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyterlite-server-extension", [7,0,1,0,,"beta",13], () => (Promise.all([__webpack_require__.e("vendors-node_modules_json5_dist_index_js-node_modules_localforage_dist_localforage_js"), __webpack_require__.e("webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel"), __webpack_require__.e("lite_server-extension_lib_index_js")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyterlite-server-extension */ "../lite/server-extension/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel/@datalayer/jupyterlite-ipykernel": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyterlite-ipykernel", [7,0,1,0,,"beta",13], () => (Promise.all([__webpack_require__.e("vendors-node_modules_comlink_dist_esm_comlink_mjs"), __webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils"), __webpack_require__.e("lite_ipykernel_lib_worker_js"), __webpack_require__.e("lite_ipykernel_lib_index_js-_d5051")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyterlite-ipykernel */ "../lite/ipykernel/lib/index.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_lumino_coreutils": [
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lumino_signaling": [
/******/ 				"webpack/sharing/consume/default/@lumino/signaling"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lumino_messaging": [
/******/ 				"webpack/sharing/consume/default/@lumino/messaging"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_coreutils": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/coreutils"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lumino_widgets": [
/******/ 				"webpack/sharing/consume/default/@lumino/widgets"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lumino_algorithm": [
/******/ 				"webpack/sharing/consume/default/@lumino/algorithm"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_services": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyter-widgets_base_jupyter-widgets_base": [
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base?a94e"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_datalayer_jupyterlite-server_datalayer_jupyterlite-server": [
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyterlite-server/@datalayer/jupyterlite-server"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"lib_components_filebrowser_FileBrowser_js-lib_components_notebook_cell_prompt_CountdownInputP-f979e0": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base?5ccc",
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls?27d1",
/******/ 				"webpack/sharing/consume/default/react-error-boundary/react-error-boundary",
/******/ 				"webpack/sharing/consume/default/react-redux/react-redux",
/******/ 				"webpack/sharing/consume/default/redux/redux",
/******/ 				"webpack/sharing/consume/default/typescript-fsa/typescript-fsa",
/******/ 				"webpack/sharing/consume/default/typescript-fsa-reducers/typescript-fsa-reducers",
/******/ 				"webpack/sharing/consume/default/redux-observable/redux-observable",
/******/ 				"webpack/sharing/consume/default/styled-components/styled-components"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyter-widgets_output_jupyter-widgets_output-webpack_sharing-ed5f68": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/outputarea",
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/output/@jupyter-widgets/output?56a9"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_codemirror_state-webpack_sharing_consume_default_codemirror_view": [
/******/ 				"webpack/sharing/consume/default/@codemirror/view",
/******/ 				"webpack/sharing/consume/default/@codemirror/state"
/******/ 			],
/******/ 			"lib_index_js": [
/******/ 				"webpack/sharing/consume/default/rxjs/rxjs?f93d",
/******/ 				"webpack/sharing/consume/default/@datalayer/typescript-fsa-redux-observable/@datalayer/typescript-fsa-redux-observable",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/documentsearch",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/translation",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/cells",
/******/ 				"webpack/sharing/consume/default/@lumino/commands",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/codemirror",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/completer",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/@jupyter/ydoc",
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/html-manager/@jupyter-widgets/html-manager",
/******/ 				"webpack/sharing/consume/default/codemirror/codemirror",
/******/ 				"webpack/sharing/consume/default/@codemirror/lang-python/@codemirror/lang-python",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/json-extension",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/javascript-extension",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/mathjax-extension",
/******/ 				"webpack/sharing/consume/default/marked/marked",
/******/ 				"webpack/sharing/consume/default/@lumino/disposable",
/******/ 				"webpack/sharing/consume/default/@lumino/properties",
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/output/@jupyter-widgets/output?aa08",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/console",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docmanager",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/filebrowser",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/fileeditor",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/terminal"
/******/ 			],
/******/ 			"lib_jupyter_lab_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/settingregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/launcher",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/codeeditor"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_default_lezer_common": [
/******/ 				"webpack/sharing/consume/default/@codemirror/language",
/******/ 				"webpack/sharing/consume/default/@lezer/common"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lezer_highlight": [
/******/ 				"webpack/sharing/consume/default/@lezer/highlight"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_datalayer_jupyterlite-kernel_datalayer_jupyterlite-kernel": [
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyterlite-kernel/@datalayer/jupyterlite-kernel"
/******/ 			],
/******/ 			"lite_kernel_lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/observables"
/******/ 			],
/******/ 			"lite_server_lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@lumino/application"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_lumino_domutils": [
/******/ 				"webpack/sharing/consume/default/@lumino/domutils"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyter-widgets_controls_jupyter-widgets_controls": [
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls?13a6"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_rxjs_rxjs": [
/******/ 				"webpack/sharing/consume/default/rxjs/rxjs?4a1c"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel-extension_datalayer_jupyterli-4c7967": [
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel-extension/@datalayer/jupyterlite-ipykernel-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_datalayer_jupyterlite-server-extension_datalayer_jupyterlite--eaaa26": [
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyterlite-server-extension/@datalayer/jupyterlite-server-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_datalayer_jupyterlite-ipykernel_datalayer_jupyterlite-ipykernel": [
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyterlite-ipykernel/@datalayer/jupyterlite-ipykernel"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		__webpack_require__.b = document.baseURI || self.location.href;
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"@datalayer/jupyter-react": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(codemirror_(language\-webpack_sharing_consume_default_lezer_common|state\-webpack_sharing_consume_default_codemirror_view)|datalayer_jupyterlite\-(ipykernel(\-extension_datalayer_jupyterli\-4c7967|_datalayer_jupyterlite\-ipykernel)|server(\-extension_datalayer_jupyterlite\-\-eaaa26|_datalayer_jupyterlite\-server)|kernel_datalayer_jupyterlite\-kernel)|jupyter(\-widgets_(base_jupyter\-widgets_base|controls_jupyter\-widgets_controls|output_jupyter\-widgets_output\-webpack_sharing\-ed5f68)|lab_(coreutil|service)s)|l(umino_(((core|dom)util|widget)s|(messag|signal)ing|algorithm)|ezer_highlight)|r(eact(|\-dom)|xjs_rxjs))$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunk_datalayer_jupyter_react"] = self["webpackChunk_datalayer_jupyter_react"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/@datalayer/jupyter-react");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB)["@datalayer/jupyter-react"] = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.dd42360f5cb427d7f19d.js.map