"use strict";
/* eslint-disable prettier/prettier */
Object.defineProperty(exports, "__esModule", { value: true });
exports.toggle_admonition = void 0;
var notebook_1 = require("@jupyterlab/notebook");
var FENCE = '````';
/* works on the active cell */
var toggle_admonition = function (notebook, admonition) {
    var activeCell = notebook === null || notebook === void 0 ? void 0 : notebook.activeCell;
    if (activeCell === undefined) {
        return;
    }
    var model = activeCell === null || activeCell === void 0 ? void 0 : activeCell.model;
    if (model === undefined) {
        return;
    }
    notebook_1.NotebookActions.changeCellType(notebook, 'markdown');
    var cell_source = model.sharedModel.getSource();
    // remove trailing newlines
    while (cell_source.endsWith('\n')) {
        cell_source = cell_source.slice(0, -1);
    }
    // does it start with an admonition?
    var turning_off = cell_source.startsWith(FENCE);
    console.debug('admonition: turning_off', turning_off);
    // a function that removes any initial white line, and any trailing white line
    // a line is considered white if it is empty or only contains whitespace
    var tidy = function (dirty) {
        var lines = dirty.split('\n');
        while (lines.length != 0 && lines[0].match(/^\s*$/)) {
            lines.shift();
        }
        while (lines.length != 0 && lines[lines.length - 1].match(/^\s*$/)) {
            lines.pop();
        }
        return lines.join('\n');
    };
    var new_source;
    if (turning_off) {
        new_source = tidy(cell_source
            .replace(RegExp("^".concat(FENCE, " *{[a-zA-Z]+}")), '')
            .replace(RegExp("\n".concat(FENCE, "$")), ''));
    }
    else {
        new_source = "".concat(FENCE, "{").concat(admonition, "}\n").concat(tidy(cell_source), "\n").concat(FENCE);
    }
    model.sharedModel.setSource(new_source);
};
exports.toggle_admonition = toggle_admonition;
