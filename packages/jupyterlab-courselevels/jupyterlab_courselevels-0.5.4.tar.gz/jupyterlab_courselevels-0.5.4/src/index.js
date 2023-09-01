"use strict";
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */
Object.defineProperty(exports, "__esModule", { value: true });
var apputils_1 = require("@jupyterlab/apputils");
var notebook_1 = require("@jupyterlab/notebook");
var disposable_1 = require("@lumino/disposable");
var apputils_2 = require("@jupyterlab/apputils");
var jupyterlab_celltagsclasses_1 = require("jupyterlab-celltagsclasses");
var jupyterlab_celltagsclasses_2 = require("jupyterlab-celltagsclasses");
var admonitions_1 = require("./admonitions");
var plugin = {
    id: 'jupyterlab-courselevels:plugin',
    autoStart: true,
    requires: [apputils_1.ICommandPalette, notebook_1.INotebookTracker],
    activate: function (app, palette, notebookTracker) {
        console.log('extension jupyterlab-courselevels is activating');
        // https://lumino.readthedocs.io/en/1.x/api/commands/interfaces/commandregistry.ikeybindingoptions.html
        // The supported modifiers are: Accel, Alt, Cmd, Ctrl, and Shift. The Accel
        // modifier is translated to Cmd on Mac and Ctrl on all other platforms. The
        // Cmd modifier is ignored on non-Mac platforms.
        // Alt is option on mac
        var cell_toggle_level = function (cell, level) {
            switch (level) {
                case 'basic':
                    if ((0, jupyterlab_celltagsclasses_1.md_has)(cell, 'tags', 'level_basic')) {
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_basic');
                    }
                    else {
                        (0, jupyterlab_celltagsclasses_1.md_insert)(cell, 'tags', 'level_basic');
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_intermediate');
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    break;
                case 'intermediate':
                    if ((0, jupyterlab_celltagsclasses_1.md_has)(cell, 'tags', 'level_intermediate')) {
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_intermediate');
                    }
                    else {
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_basic');
                        (0, jupyterlab_celltagsclasses_1.md_insert)(cell, 'tags', 'level_intermediate');
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    break;
                case 'advanced':
                    if ((0, jupyterlab_celltagsclasses_1.md_has)(cell, 'tags', 'level_advanced')) {
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_advanced');
                    }
                    else {
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_basic');
                        (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_intermediate');
                        (0, jupyterlab_celltagsclasses_1.md_insert)(cell, 'tags', 'level_advanced');
                    }
                    break;
                default:
                    (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_basic');
                    (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_intermediate');
                    (0, jupyterlab_celltagsclasses_1.md_remove)(cell, 'tags', 'level_advanced');
            }
        };
        var toggle_level = function (level) {
            (0, jupyterlab_celltagsclasses_2.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses_2.Scope.Active, function (cell) {
                cell_toggle_level(cell, level);
            });
        };
        var command;
        var _loop_1 = function (level, key) {
            command = "courselevels:toggle-level-".concat(level);
            app.commands.addCommand(command, {
                label: "toggle ".concat(level, " level"),
                execute: function () { return toggle_level(level); }
            });
            palette.addItem({ command: command, category: 'CourseLevels' });
            app.commands.addKeyBinding({ command: command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' });
        };
        for (var _i = 0, _a = [
            ['basic', 'Ctrl X'],
            ['intermediate', 'Ctrl Y'],
            ['advanced', 'Ctrl Z'],
        ]; _i < _a.length; _i++) {
            var _b = _a[_i], level = _b[0], key = _b[1];
            _loop_1(level, key);
        }
        var toggle_frame = function () {
            (0, jupyterlab_celltagsclasses_2.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses_2.Scope.Active, function (cell) {
                (0, jupyterlab_celltagsclasses_1.md_toggle)(cell, 'tags', 'framed_cell');
            });
        };
        command = 'courselevels:toggle-frame';
        app.commands.addCommand(command, {
            label: 'toggle frame',
            execute: function () { return toggle_frame(); }
        });
        palette.addItem({ command: command, category: 'CourseLevels' });
        app.commands.addKeyBinding({ command: command, keys: ['Ctrl \\', 'Ctrl M'], selector: '.jp-Notebook' });
        var toggle_licence = function () {
            (0, jupyterlab_celltagsclasses_2.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses_2.Scope.Active, function (cell) {
                (0, jupyterlab_celltagsclasses_1.md_toggle)(cell, 'tags', 'licence');
            });
        };
        command = 'courselevels:toggle-licence';
        app.commands.addCommand(command, {
            label: 'toggle licence',
            execute: function () { return toggle_licence(); }
        });
        palette.addItem({ command: command, category: 'CourseLevels' });
        app.commands.addKeyBinding({ command: command, keys: ['Ctrl \\', 'Ctrl L'], selector: '.jp-Notebook' });
        // the buttons in the toolbar
        var find_spacer = function (panel) {
            var index = 0;
            for (var _i = 0, _a = panel.toolbar.children(); _i < _a.length; _i++) {
                var child = _a[_i];
                if (child.node.classList.contains('jp-Toolbar-spacer')) {
                    return index;
                }
                else {
                    index += 1;
                }
            }
            return 0;
        };
        var BasicButton = /** @class */ (function () {
            function BasicButton() {
            }
            BasicButton.prototype.createNew = function (panel, context) {
                var button = new apputils_2.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-pointer',
                    onClick: function () { return toggle_level('basic'); },
                    tooltip: 'Toggle basic level',
                });
                // compute where to insert it
                var index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'basicLevel', button);
                return new disposable_1.DisposableDelegate(function () {
                    button.dispose();
                });
            };
            return BasicButton;
        }());
        app.docRegistry.addWidgetExtension('Notebook', new BasicButton());
        var IntermediateButton = /** @class */ (function () {
            function IntermediateButton() {
            }
            IntermediateButton.prototype.createNew = function (panel, context) {
                var button = new apputils_2.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-peace',
                    onClick: function () { return toggle_level('intermediate'); },
                    tooltip: 'Toggle intermediate level',
                });
                // compute where to insert it
                var index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'intermediateLevel', button);
                return new disposable_1.DisposableDelegate(function () {
                    button.dispose();
                });
            };
            return IntermediateButton;
        }());
        app.docRegistry.addWidgetExtension('Notebook', new IntermediateButton());
        var AdvancedButton = /** @class */ (function () {
            function AdvancedButton() {
            }
            AdvancedButton.prototype.createNew = function (panel, context) {
                var button = new apputils_2.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'far fa-hand-spock',
                    onClick: function () { return toggle_level('advanced'); },
                    tooltip: 'Toggle advanced level',
                });
                // compute where to insert it
                var index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'advancedLevel', button);
                return new disposable_1.DisposableDelegate(function () {
                    button.dispose();
                });
            };
            return AdvancedButton;
        }());
        app.docRegistry.addWidgetExtension('Notebook', new AdvancedButton());
        var FrameButton = /** @class */ (function () {
            function FrameButton() {
            }
            FrameButton.prototype.createNew = function (panel, context) {
                var button = new apputils_2.ToolbarButton({
                    className: 'courselevels-button',
                    iconClass: 'fas fa-crop-alt',
                    onClick: function () { return toggle_frame(); },
                    tooltip: 'Toggle frame around cell',
                });
                // compute where to insert it
                var index = find_spacer(panel);
                panel.toolbar.insertItem(index, 'frameLevel', button);
                return new disposable_1.DisposableDelegate(function () {
                    button.dispose();
                });
            };
            return FrameButton;
        }());
        app.docRegistry.addWidgetExtension('Notebook', new FrameButton());
        var _loop_2 = function (name_1, key) {
            var admonition = name_1;
            command = 'courselevels:toggle-admonition';
            if (admonition !== 'admonition') {
                command += "-".concat(admonition);
            }
            app.commands.addCommand(command, {
                label: "toggle admonition ".concat(admonition),
                execute: function () {
                    var _a;
                    var notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                    if (notebook === undefined) {
                        return;
                    }
                    (0, admonitions_1.toggle_admonition)(notebook, admonition);
                }
            });
            palette.addItem({ command: command, category: 'CourseLevels' });
            if (key !== null) {
                app.commands.addKeyBinding({ command: command, keys: ['Ctrl \\', key], selector: '.jp-Notebook' });
            }
        };
        // admonitions
        for (var _c = 0, _d = [
            ['admonition', 'Ctrl A'],
            ['tip', 'Ctrl T'],
            ['note', 'Ctrl N'],
            ['attention', null],
            ['caution', null],
            ['danger', null],
            ['error', null],
            ['hint', null],
            ['important', null],
            ['seealso', null],
            ['warning', null],
        ]; _c < _d.length; _c++) {
            var _e = _d[_c], name_1 = _e[0], key = _e[1];
            _loop_2(name_1, key);
        }
    }
};
exports.default = plugin;
