/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/constants.ts":
/*!**************************!*\
  !*** ./src/constants.ts ***!
  \**************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FILE_URI_PREFIX_RE = void 0;
exports.FILE_URI_PREFIX_RE = /^file:\/\//;


/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

//#!/usr/bin/env osascript -l JavaScript

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
var constants_1 = __webpack_require__(/*! ./constants */ "./src/constants.ts");
var itunes_1 = __importDefault(__webpack_require__(/*! ./itunes */ "./src/itunes.ts"));
ObjC.import('AppKit');
ObjC.import('Foundation');
ObjC.import('stdlib');
var it = new itunes_1.default();
// FIXME Read arguments
var dir = it.finder.home().folders.byName('Music').folders.byName('import');
console.log('Deleting orphaned tracks');
it.deleteOrphanedTracks();
console.log('Updating iTunes track list');
it.addTracksAtPath(dir);
var ratings = {};
console.log('Building basename:track hash');
for (var _i = 0, _a = it.library.tracks(); _i < _a.length; _i++) {
    var track = _a[_i];
    ratings[ObjC.unwrap($.NSString.stringWithString(track.location().toString()).lastPathComponent)] =
        track;
}
console.log('Setting ratings');
for (var _b = 0, _c = ObjC.unwrap($.NSString.stringWithContentsOfFileUsedEncodingError(dir.items.byName('.ratings').url().replace(constants_1.FILE_URI_PREFIX_RE, ''), $.NSUTF8StringEncoding, null))
    .split('\n')
    .map(function (l) { return l.trim(); })
    .filter(function (x) { return !!x; })
    .map(function (l) { return l.split(' ', 2); })
    .map(function (_a) {
    var ratingStr = _a[0], filename = _a[1];
    return [(parseInt(ratingStr, 10) / 5) * 100, filename];
}); _b < _c.length; _b++) {
    var _d = _c[_b], rating = _d[0], filename = _d[1];
    if (!(filename in ratings)) {
        throw new Error("File not found: ".concat(filename));
    }
    ratings[filename]().rating = rating;
}
console.log('Syncing device if present');
try {
    it.syncDevice();
}
catch (error) {
    /* empty */
}
$.exit(0);


/***/ }),

/***/ "./src/itunes.ts":
/*!***********************!*\
  !*** ./src/itunes.ts ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
var constants_1 = __webpack_require__(/*! ./constants */ "./src/constants.ts");
var lawbio = 'launchAppWithBundleIdentifierOptionsAdditionalEventParamDescriptorLaunchIdentifier';
var ITunes = /** @class */ (function () {
    function ITunes() {
        this.finder = Application('Finder');
    }
    ITunes.prototype.running = function () {
        for (var _i = 0, _a = ObjC.unwrap($.NSWorkspace.sharedWorkspace.runningApplications); _i < _a.length; _i++) {
            var app = _a[_i];
            if (typeof app.bundleIdentifier.isEqualToString !== 'undefined' &&
                app.bundleIdentifier.isEqualToString('com.apple.iTunes')) {
                return true;
            }
        }
        return false;
    };
    Object.defineProperty(ITunes.prototype, "itunes", {
        get: function () {
            if (this.pItunes) {
                return this.pItunes;
            }
            if (!this.running()) {
                $.NSWorkspace.sharedWorkspace[lawbio]('com.apple.iTunes', $.NSWorkspaceLaunchAsync | $.NSWorkspaceLaunchAndHide, $.NSAppleEventDescriptor.nullDescriptor, null);
                delay(3);
            }
            this.pItunes = Application('iTunes');
            var se = Application('System Events');
            var proc = se.processes.byName('iTunes');
            this.pDevicesMenuItems = proc.menuBars[0].menuBarItems
                .byName('File')
                .menus[0].menuItems.byName('Devices')
                .menus[0].menuItems();
            return this.pItunes;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ITunes.prototype, "library", {
        get: function () {
            if (this.pLibrary) {
                return this.pLibrary;
            }
            for (var _i = 0, _a = this.itunes.sources(); _i < _a.length; _i++) {
                var source = _a[_i];
                if (source.name() === 'Library') {
                    this.pLibrary = source;
                    break;
                }
            }
            return this.pLibrary;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ITunes.prototype, "currentTrack", {
        get: function () {
            try {
                return this.itunes.currentTrack;
            }
            catch (e) {
                return null;
            }
        },
        enumerable: false,
        configurable: true
    });
    ITunes.prototype.deleteOrphanedTracks = function () {
        var ret = [];
        for (var _i = 0, _a = this.library.tracks(); _i < _a.length; _i++) {
            var track = _a[_i];
            var name_1 = track.name();
            var loc = void 0;
            try {
                loc = track.location();
            }
            catch (e) {
                console.debug("Removing ".concat(name_1));
                ret.push(track);
                track.delete();
                continue;
            }
            if (!loc || !this.finder.exists(loc)) {
                console.debug("Removing ".concat(name_1));
                ret.push(track);
                track.delete();
            }
        }
        return ret;
    };
    /**
     * Root must be a Finder folder item
     * `finder.home().folders.byName('Music').folders.byName('import');`
     */
    ITunes.prototype.addTracksAtPath = function (root) {
        var paths = root.entireContents().map(function (x) { return Path(x.url().replace(constants_1.FILE_URI_PREFIX_RE, '')); });
        this.itunes.add(paths, {
            to: this.library,
        });
        // Refresh all tracks in case some changes do not get detected
        var results = [];
        for (var _i = 0, _a = this.library.tracks(); _i < _a.length; _i++) {
            var track = _a[_i];
            results.push(this.itunes.refresh(track));
        }
        return results;
    };
    ITunes.prototype.clickDevicesMenuItem = function (regex) {
        this.itunes.activate();
        for (var i = 0; i < this.pDevicesMenuItems.length; i++) {
            var item = this.pDevicesMenuItems[i];
            if (regex.test(item.title()) && item.enabled()) {
                item.click();
                return true;
            }
        }
        return false;
    };
    ITunes.prototype.syncDevice = function () {
        return this.clickDevicesMenuItem(/^Sync /);
    };
    ITunes.prototype.backupDevice = function () {
        return this.clickDevicesMenuItem(/^Back Up$/);
    };
    ITunes.prototype.transferPurchasesFromDevice = function () {
        return this.clickDevicesMenuItem(/^Transfer Purchases from /);
    };
    return ITunes;
}());
exports["default"] = ITunes;


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
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./src/index.ts");
/******/ 	
/******/ })()
;