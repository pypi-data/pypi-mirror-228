"use strict";
(self["webpackChunk_datalayer_jupyter_functions"] = self["webpackChunk_datalayer_jupyter_functions"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-ca7f34"],{

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!*********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".dla-Container {\n    overflow-y: visible;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;IACI,mBAAmB;AACvB","sourcesContent":[".dla-Container {\n    overflow-y: visible;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!**********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../../node_modules/css-loader/dist/cjs.js!./base.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../icons/react/data1/esm/DaskIcon.js":
/*!***********************************************!*\
  !*** ../../icons/react/data1/esm/DaskIcon.js ***!
  \***********************************************/
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

function DaskIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    viewBox: "0 0 20 20",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#FFC11E' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#FFC11E') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M5.383 6.332l5.094-2.902a.158.158 0 00.082-.137V1.551a.822.822 0 00-.317-.668.819.819 0 00-.898-.059L2.219 4.883a.801.801 0 00-.406.691l-.004 9.164c0 .258.109.512.316.668.27.203.613.223.898.059l1.512-.856a.17.17 0 00.078-.14l.004-6.828c0-.543.293-1.04.766-1.309zm0 0",
    clipRule: "evenodd"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#EF1161' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EF1161') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M17.594 5.016a.826.826 0 00-.809 0L9.656 9.074a.8.8 0 00-.402.692l-.004 9.199c0 .289.152.547.406.691a.808.808 0 00.809 0l7.125-4.058a.796.796 0 00.406-.692L18 5.711c0-.29-.152-.55-.406-.695zm0 0",
    clipRule: "evenodd"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#FC6E6B' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#FC6E6B') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M9.297 8.457L14 5.781a.16.16 0 00.082-.14l.004-2.024a.828.828 0 00-.316-.668.805.805 0 00-.899-.058L10.918 4 5.742 6.945a.807.807 0 00-.406.696v6.921l-.004 2.243c0 .254.11.511.316.668a.82.82 0 00.899.058l1.902-1.082a.164.164 0 00.082-.14V9.766c.004-.54.293-1.04.766-1.309zm0 0",
    clipRule: "evenodd"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(DaskIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/data1/esm/PyTorchIcon.js":
/*!**************************************************!*\
  !*** ../../icons/react/data1/esm/PyTorchIcon.js ***!
  \**************************************************/
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

function PyTorchIcon({
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
    fill: colored ? '#EE4C2C' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EE4C2C') ? 'white' : 'currentColor'),
    d: "M15.882 5.877L14.43 7.33a6.218 6.218 0 010 8.782 6.218 6.218 0 01-8.782 0 6.218 6.218 0 010-8.782L9.52 3.457l.484-.553V0L4.127 5.877a8.221 8.221 0 000 11.686 8.22 8.22 0 0011.685 0c3.32-3.25 3.32-8.505.07-11.686z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#EE4C2C' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EE4C2C') ? 'white' : 'currentColor'),
    d: "M12.977 5.462a1.106 1.106 0 100-2.212 1.106 1.106 0 000 2.212z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(PyTorchIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/data2/esm/EjectIconLabIcon.js":
/*!*******************************************************!*\
  !*** ../../icons/react/data2/esm/EjectIconLabIcon.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/labicon */ "../../../node_modules/@jupyterlab/ui-components/lib/icon/labicon.js");
/* harmony import */ var _EjectIcon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./EjectIcon.svg */ "../../icons/react/data2/esm/EjectIcon.svg");


const ejectIconLabIcon = new _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@datalayer/icons:eject',
    svgstr: _EjectIcon_svg__WEBPACK_IMPORTED_MODULE_1__,
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ejectIconLabIcon);

/***/ }),

/***/ "../../icons/react/data2/esm/TensorFlowIcon.js":
/*!*****************************************************!*\
  !*** ../../icons/react/data2/esm/TensorFlowIcon.js ***!
  \*****************************************************/
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

function TensorFlowIcon({
  title,
  titleId,
  size,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: "none",
    "aria-hidden": "true",
    viewBox: "0 0 20 20",
    ref: svgRef,
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#E55B2D",
    d: "M11.332 3.077v3.077l5.33 3.077V6.154l-5.33-3.077zM.674 6.154V9.23l2.664 1.538V7.692L.674 6.154zm7.993 1.538L6.003 9.231v9.23L8.667 20v-6.154l2.665 1.539v-3.077l-2.665-1.539V7.692z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#ED8E24",
    d: "M11.332 3.077L3.338 7.692v3.077l5.33-3.077v3.077l2.664-1.538V3.077zm7.994 1.538l-2.665 1.539V9.23l2.665-1.539V4.615zm-5.33 6.154l-2.664 1.539v3.077l2.665-1.539V10.77zm-2.664 4.616l-2.665-1.539V20l2.665-1.538v-3.077z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#F8BF3C",
    d: "M11.332 0L.674 6.154l2.664 1.538 7.994-4.615 5.33 3.077 2.665-1.539L11.331 0zm0 9.23l-2.665 1.54 2.665 1.538 2.665-1.539-2.665-1.538z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(TensorFlowIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "./lib/Tabs.js":
/*!*********************!*\
  !*** ./lib/Tabs.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ThemeProvider.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/BaseStyles.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/UnderlineNav/index.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _tabs_Tab1__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/Tab1 */ "./lib/tabs/Tab1.js");
/* harmony import */ var _tabs_Tab2__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/Tab2 */ "./lib/tabs/Tab2.js");
/* harmony import */ var _tabs_Tab3__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/Tab3 */ "./lib/tabs/Tab3.js");
/* harmony import */ var _tabs_Tab4__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/Tab4 */ "./lib/tabs/Tab4.js");
/* harmony import */ var _tabs_Tab5__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./tabs/Tab5 */ "./lib/tabs/Tab5.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");










const Tabs = () => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    const [version, setVersion] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('config')
            .then(data => {
            setVersion(data.version);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_functions extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { style: { maxWidth: 700 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav, { "aria-label": "jupyter-functions", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": tab === 1 ? "page" : undefined, "aria-label": "tab-1", icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__.CpuIcon, onSelect: e => { e.preventDefault(); setTab(1); }, children: "Kernels" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": tab === 2 ? "page" : undefined, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__.CodeIcon, counter: 6, "aria-label": "tab-2", onSelect: e => { e.preventDefault(); setTab(2); }, children: "Notebooks" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": tab === 3 ? "page" : undefined, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__.AlertIcon, "aria-label": "tab-3", onSelect: e => { e.preventDefault(); setTab(3); }, children: "Warnings" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": tab === 4 ? "page" : undefined, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__.HistoryIcon, counter: 7, "aria-label": "tab-4", onSelect: e => { e.preventDefault(); setTab(4); }, children: "History" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": tab === 5 ? "page" : undefined, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_7__.CommentDiscussionIcon, "aria-label": "tab-5", onSelect: e => { e.preventDefault(); setTab(5); }, children: "More" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { m: 3, children: [(tab === 1) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_Tab1__WEBPACK_IMPORTED_MODULE_8__["default"], { version: version }), (tab === 2) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_Tab2__WEBPACK_IMPORTED_MODULE_9__["default"], {}), (tab === 3) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_Tab3__WEBPACK_IMPORTED_MODULE_10__["default"], {}), (tab === 4) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_Tab4__WEBPACK_IMPORTED_MODULE_11__["default"], {}), (tab === 5) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_Tab5__WEBPACK_IMPORTED_MODULE_12__["default"], {})] })] }) }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tabs);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter_functions', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
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
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _datalayer_icons_react_data2_EjectIconLabIcon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react/data2/EjectIconLabIcon */ "../../icons/react/data2/esm/EjectIconLabIcon.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _ws__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ws */ "./lib/ws.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");








/**
 * The command IDs used by the jupyter-functions plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-jupyter-functions-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/jupyter-functions extension.
 */
const plugin = {
    id: '@datalayer/jupyter-functions:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    activate: (app, palette, settingRegistry, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Show Jupyter Functions',
            label: 'Jupyter Functions',
            icon: _datalayer_icons_react_data2_EjectIconLabIcon__WEBPACK_IMPORTED_MODULE_4__["default"],
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_5__.CounterWidget();
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                widget.title.label = 'Jupyter Functions';
                widget.title.icon = _datalayer_icons_react_data2_EjectIconLabIcon__WEBPACK_IMPORTED_MODULE_4__["default"];
                app.shell.add(widget, 'main');
            }
        });
        const category = 'Datalayer';
        palette.addItem({ command, category });
        if (launcher) {
            launcher.add({
                command,
                category,
                rank: 3
            });
        }
        console.log('JupyterLab plugin @datalayer/jupyter-functions is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('@datalayer/jupyter-functions settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/jupyter-functions.', reason);
            });
        }
        (0,_ws__WEBPACK_IMPORTED_MODULE_6__.connect)('ws://localhost:8888/api/jupyter/jupyter_functions/echo', true);
        (0,_handler__WEBPACK_IMPORTED_MODULE_7__.requestAPI)('config')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_functions extension.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/tabs/Tab1.js":
/*!**************************!*\
  !*** ./lib/tabs/Tab1.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ActionMenu.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ActionList/index.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ProgressBar/index.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Avatar/Avatar.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/DaskIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data2/esm/TensorFlowIcon.js");




const Tab1 = (props) => {
    const { version } = props;
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { children: ["Version: ", version] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Button, { children: "Kernels" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Overlay, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { onSelect: event => console.log('New file'), children: "New kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: "Copy kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: "Edit kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Divider, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { variant: "danger", children: "Delete kernel" })] }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_4__["default"], {}) }), "Dask kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__["default"], {}) }), "PyTorch Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_6__["default"], {}) }), "Tensorflow Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_8__.LinkIcon, {}) }), "Starting..."] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_9__.ProgressBar, { progress: 80 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { src: "https://github.com/mona.png" }) }), "Me"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.Item, { variant: "danger", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_8__.AlertIcon, {}) }), "4 vulnerabilities"] })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tab1);


/***/ }),

/***/ "./lib/tabs/Tab2.js":
/*!**************************!*\
  !*** ./lib/tabs/Tab2.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/TreeView/TreeView.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Octicon/Octicon.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");



const Tab2 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.Item, { id: "", defaultExpanded: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.DirectoryIcon, {}) }), "Notebooks", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.SubTree, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.Item, { id: "src/Avatar.tsx", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "Deep learing", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffAddedIcon, color: "success.fg", "aria-label": "added" }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.Item, { id: "", current: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "AI for fun", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffModifiedIcon, color: "attention.fg", "aria-label": "modified" }) })] })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.Item, { id: "", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "README.mdx", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffModifiedIcon, color: "attention.fg", "aria-label": "modified" }) })] })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tab2);


/***/ }),

/***/ "./lib/tabs/Tab3.js":
/*!**************************!*\
  !*** ./lib/tabs/Tab3.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Button/Button.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Popover/Popover.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Heading/Heading.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");


const Tab3 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__["default"], { style: { width: 300, paddingTop: 20 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__["default"], { justifyContent: "center", display: "flex", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ButtonComponent, { variant: "primary", children: "Hello!" }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { relative: true, open: true, caret: "top", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Content, { sx: { mt: 2 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontSize: 2 }, children: "Popover heading" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "p", children: "Message about this particular piece of UI." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ButtonComponent, { children: "Got it!" })] }) })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tab3);


/***/ }),

/***/ "./lib/tabs/Tab4.js":
/*!**************************!*\
  !*** ./lib/tabs/Tab4.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/SubNav/SubNav.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Timeline/Timeline.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Octicon/Octicon.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Link/Link.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data2/esm/TensorFlowIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/DaskIcon.js");



const Tab4 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__["default"], { m: 1, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"].Links, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"].Link, { href: "#", selected: true, children: "All" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"].Link, { href: "#", children: "Recent" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"].Link, { href: "#", children: "Older" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "PyTorch Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", color: "fg.muted", muted: true, children: "Just now" })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "TensorFlow Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", color: "fg.muted", muted: true, children: "5m ago" })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"].Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "Dask Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { href: "#", color: "fg.muted", muted: true, children: "7m ago" })] })] })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tab4);


/***/ }),

/***/ "./lib/tabs/Tab5.js":
/*!**************************!*\
  !*** ./lib/tabs/Tab5.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ActionMenu.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ActionList/index.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Avatar/Avatar.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ProgressBar/index.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Button/Button.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Popover/Popover.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Heading/Heading.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/DaskIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data1/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data2/esm/TensorFlowIcon.js");




const Tab5 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Button, { children: "Menu" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Overlay, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { onSelect: event => console.log('New file'), children: "New file" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: "Copy link" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: "Edit file" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Divider, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { variant: "danger", children: "Delete file" })] }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_3__["default"], {}) }), "Dask kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_4__["default"], {}) }), "PyTorch Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_5__["default"], {}) }), "Tensorflow Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_6__.LinkIcon, {}) }), "github.com/primer"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { variant: "danger", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_6__.AlertIcon, {}) }), "4 vulnerabilities"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { src: "https://github.com/mona.png" }) }), "mona"] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__.ProgressBar, { progress: 80 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_9__["default"], { style: { width: 300, paddingTop: 20 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_9__["default"], { justifyContent: "center", display: "flex", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__.ButtonComponent, { variant: "primary", children: "Hello!" }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_11__["default"], { relative: true, open: true, caret: "top", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_11__["default"].Content, { sx: { mt: 2 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_12__["default"], { sx: { fontSize: 2 }, children: "Popover heading" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_13__["default"], { as: "p", children: "Message about this particular piece of UI." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__.ButtonComponent, { children: "Got it!" })] }) })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Tab5);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CounterWidget": () => (/* binding */ CounterWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Tabs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Tabs */ "./lib/Tabs.js");



class CounterWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.addClass('dla-Container');
    }
    render() {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_Tabs__WEBPACK_IMPORTED_MODULE_2__["default"], {});
    }
}


/***/ }),

/***/ "./lib/ws.js":
/*!*******************!*\
  !*** ./lib/ws.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "connect": () => (/* binding */ connect),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
const connect = (address, retry) => {
    const ws = new WebSocket(address);
    ws.onerror = (event) => {
        console.error('---', event);
    };
    ws.onmessage = (message) => {
        console.log('---', message);
    };
    ws.onopen = (event) => {
        console.log('---', event);
        ws.send('ping');
    };
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (connect);


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
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../../icons/react/data2/esm/EjectIcon.svg":
/*!*************************************************!*\
  !*** ../../icons/react/data2/esm/EjectIcon.svg ***!
  \*************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 72 72\" fill=\"currentColor\" aria-hidden=\"true\">\n  <path fill=\"none\" stroke=\"#000\" stroke-linejoin=\"round\" stroke-miterlimit=\"10\" stroke-width=\"2\" d=\"M19.06 55.61c.485.178 1.03.297 1.576.297.849 0 1.697-.297 2.424-.772l30-15.98.303-.297c.788-.772 1.212-1.723 1.212-2.792s-.424-2.08-1.212-2.792l-.303-.297-30-16.1c-1.091-.832-2.667-1.01-4-.475-1.515.594-2.485 2.079-2.485 3.683v31.84c0 1.604.97 3.089 2.485 3.683z\" transform=\"matrix(0 -.9544 .9545 0 1.727 66.7)\"/>\n  <path fill=\"none\" stroke=\"#000\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-miterlimit=\"10\" stroke-width=\"2\" d=\"M17 57.38h38\"/>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-ca7f34.414f680a8c64a441cc74.js.map