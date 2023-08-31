(function () {
    function h (unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function hasOwn (object, key) {
        return object ? Object.prototype.hasOwnProperty.call(object, key) : false;
    }

    function uuid () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
            .replace(/[xy]/g, function (c) {
                const r = Math.random() * 16 | 0,
                    v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
    }

    function removeErrorMessages (container) {
        container
            .querySelectorAll(':scope > .help-block.help-critical')
            .forEach(function (element) { element.remove() });
    };

    function addErrorMessages (container, messages) {
        messages.forEach(function (message) {
            const errorElement = document.createElement('p');
            errorElement.classList.add('help-block');
            errorElement.classList.add('help-critical');
            errorElement.innerHTML = h(message);
            container.insertBefore(errorElement, container.childNodes[0]);
        });
    };

    class WagtailSBStructBlock {
        constructor(blockDef, placeholder, prefix, initialState, initialError) {
            const state = initialState || {};

            this.blockDef = blockDef;
            this.type = blockDef.name;

            this.childBlocks = {};

            this.settingsFields = blockDef.meta.settingsFields || [];

            if (blockDef.meta.formTemplate) {
                const html = blockDef.meta.formTemplate.replace(/__PREFIX__/g, prefix);
                const dom = $(html);

                $(placeholder).replaceWith(dom);

                const blockErrors = initialError?.blockErrors || {};

                this.blockDef.childBlockDefs.forEach((childBlockDef) => {

                    const childBlockElement = dom
                        .find('[data-structblock-child="' + childBlockDef.name + '"]')
                        .get(0);
                    const childBlock = childBlockDef.render(
                        childBlockElement,
                        prefix + '-' + childBlockDef.name,
                        state[childBlockDef.name],
                        blockErrors[childBlockDef.name],
                    );
                    this.childBlocks[childBlockDef.name] = childBlock;
                });

                this.container = dom;
            } else {
                this.contentUuid = uuid();
                this.settingsUuid = uuid();

                const dom = $(`
                    <div class="${h(this.blockDef.meta.classname || '')}">
                    </div>
                `);

                $(placeholder).replaceWith(dom);

                this.contentsPanel = dom;
                this.settingsPanel = null;

                if (this.settingsFields.length) {
                    const tabsLabelContentsId = `${this.contentUuid}-tabs-label-content`;
                    const tabsPanelContentsId = `${this.contentUuid}-tabs-panel-content`;
                    const tabsLabelContents = $(
                        `<a
                            id="${tabsLabelContentsId}"
                            href="#${tabsPanelContentsId}"
                            class="sb-tabs__tab"
                            style="padding:0.5rem 0 0.5rem 0;"
                            aria-selected="true"
                            aria-controls="${tabsPanelContentsId}">
                            Content
                        </a>`
                    )
                    const tabsPanelContents = $(
                        `<section
                            id="${tabsPanelContentsId}"
                            class="sb-tabs__panel"
                            aria-labelledby="${tabsLabelContentsId}">
                        </section>`
                    )

                    const tabsLabelSettingsId = `${this.settingsUuid}-tabs-label-settings`;
                    const tabsPanelSettingsId = `${this.settingsUuid}-tabs-panel-settings`;
                    const tabsLabelSettings = $(
                        `<a
                            id="${tabsLabelSettingsId}"
                            href="#${tabsPanelSettingsId}"
                            class="sb-tabs__tab"
                            style="padding:0.5rem 0 0.5rem 0;"
                            aria-selected="false"
                            aria-controls="${tabsPanelSettingsId}">
                            Settings
                        </a>`
                    )
                    const tabsPanelSettings = $(
                        `<section
                            id="${tabsPanelSettingsId}"
                            class="sb-tabs__panel"
                            aria-labelledby="${tabsLabelSettingsId}">
                        </section>`
                    )

                    const tabsLabels = $(
                        `<div class="sb-tabs__wrapper" style="margin-bottom:1rem;">
                            <div class="sb-tabs__list" style="padding:0;">
                            </div>
                        </div>`
                    );

                    const tabsPanels = $(
                        `<div class="tab-content" style="padding:0;">
                        </div>`
                    );

                    const tabs = $(
                        `<div class="sb-tabs">
                        </div>`
                    );

                    tabsLabels.find('.sb-tabs__list').append(tabsLabelContents);
                    tabsLabels.find('.sb-tabs__list').append(tabsLabelSettings);

                    tabsPanels.append(tabsPanelContents);
                    tabsPanels.append(tabsPanelSettings);

                    tabs.append(tabsLabels);
                    tabs.append(tabsPanels);

                    dom.append(tabs);

                    $(`#${tabsPanelSettingsId}`).hide();

                    $(`#${tabsLabelContentsId}`).replaceWith($(`#${tabsLabelContentsId}`).clone().unbind().off()).unbind().off();
                    $(`#${tabsLabelSettingsId}`).replaceWith($(`#${tabsLabelSettingsId}`).clone().unbind().off()).unbind().off();

                    $(`#${tabsLabelContentsId}`).on('click', function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        $(`#${tabsLabelSettingsId}`).attr('aria-selected', 'false');
                        $(`#${tabsPanelSettingsId}`).hide();

                        $(this).attr('aria-selected', 'true');
                        $(`#${tabsPanelContentsId}`).show();
                    });

                    $(`#${tabsLabelSettingsId}`).on('click', function (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        $(`#${tabsLabelContentsId}`).attr('aria-selected', 'false');
                        $(`#${tabsPanelContentsId}`).hide();

                        $(this).attr('aria-selected', 'true');
                        $(`#${tabsPanelSettingsId}`).show();
                    });

                    this.contentsPanel = tabsPanelContents;
                    this.settingsPanel = tabsPanelSettings;

                    this.contentsLabel = $(`#${tabsLabelContentsId}`);
                    this.settingsLabel = $(`#${tabsLabelSettingsId}`);
                }

                if (this.blockDef.meta.helpText) {
                    contentsPanel.append(`
                        <div class="c-sf-help">
                            <div class="help">
                                ${this.blockDef.meta.helpText}
                            </div>
                        </div>
                    `);
                }

                this.blockDef.childBlockDefs.forEach((childBlockDef) => {
                    const childDom = $(`
                        <div data-contentpath="${childBlockDef.name}">
                            <label class="w-field__label">
                                ${h(childBlockDef.meta.label)}
                                ${childBlockDef.meta.required ? '<span class="w-required-mark">*</span>' : ''}
                            </label>
                            <div data-streamfield-block></div>
                        </div>
                    `);

                    if (this.settingsFields.includes(childBlockDef.name)) {
                        this.settingsPanel.append(childDom);
                    } else {
                        this.contentsPanel.append(childDom);
                    }

                    const childBlockElement = childDom
                        .find('[data-streamfield-block]')
                        .get(0);

                    console.log(initialError)

                    const labelElement = childDom.find('label').get(0);
                    const blockErrors = initialError?.blockErrors || {};
                    const childBlock = childBlockDef.render(
                        childBlockElement,
                        prefix + '-' + childBlockDef.name,
                        state[childBlockDef.name],
                        blockErrors[childBlockDef.name],
                        new Map(),
                    );

                    this.childBlocks[childBlockDef.name] = childBlock;

                    if (childBlock.idForLabel) {
                        labelElement.setAttribute('for', childBlock.idForLabel);
                    }
                });

                this.container = dom;
            }
        }

        setState (state) {
            // eslint-disable-next-line guard-for-in
            for (const name in state) {
                this.childBlocks[name].setState(state[name]);
            }
        }

        setError (error) {
            if (!error) return;

            // Non block errors
            const container = this.container[0];

            removeErrorMessages(container);

            if (error.messages) {
                addErrorMessages(container, error.messages);
            }

            if (error.blockErrors) {
                let settingsErrorsCount = 0;
                let contentsErrorsCount = 0;

                for (const blockName in error.blockErrors) {
                    if (hasOwn(error.blockErrors, blockName)) {
                        this.childBlocks[blockName].setError(error.blockErrors[blockName]);

                        if (this.settingsFields.includes(blockName)) {
                            settingsErrorsCount += 1;
                        } else {
                            contentsErrorsCount += 1;
                        }
                    }
                }

                if (settingsErrorsCount > 0) {
                    console.log("settingsErrorsCount", settingsErrorsCount)
                    this.settingsLabel.append(
                        $(`
                            <div class="sb-tabs__errors !w-flex" data-w-count-active-class="!w-flex">
                                <span aria-hidden="true" >${settingsErrorsCount}</span>
                                <span class="w-sr-only">(<span>${settingsErrorsCount} error${settingsErrorsCount > 1 ? 's' : ''}</span>)</span>
                            </div>
                        `)
                    )
                }

                if (contentsErrorsCount > 0) {
                    console.log("contentsErrorsCount", contentsErrorsCount)
                    this.contentsLabel.append(
                        $(`
                            <div class="sb-tabs__errors !w-flex" data-w-count-active-class="!w-flex">
                                <span aria-hidden="true" >${contentsErrorsCount}</span>
                                <span class="w-sr-only">(<span>${contentsErrorsCount} error${contentsErrorsCount > 1 ? 's' : ''}</span>)</span>
                            </div>
                        `)
                    )
                }
            }
        }

        getState () {
            const state = {};
            // eslint-disable-next-line guard-for-in
            for (const name in this.childBlocks) {
                state[name] = this.childBlocks[name].getState();
            }
            return state;
        }

        getDuplicatedState () {
            const state = {};
            // eslint-disable-next-line guard-for-in
            for (const name in this.childBlocks) {
                const block = this.childBlocks[name];
                state[name] =
                    block.getDuplicatedState === undefined
                        ? block.getState()
                        : block.getDuplicatedState();
            }
            return state;
        }

        getValue () {
            const value = {};
            // eslint-disable-next-line guard-for-in
            for (const name in this.childBlocks) {
                value[name] = this.childBlocks[name].getValue();
            }
            return value;
        }

        getTextLabel (opts) {
            if (this.blockDef.meta.labelFormat) {
                /* use labelFormat - regexp replace any field references like '{first_name}'
                with the text label of that sub-block */
                return this.blockDef.meta.labelFormat.replace(
                    /\{(\w+)\}/g,
                    (tag, blockName) => {
                        const block = this.childBlocks[blockName];
                        if (block && block.getTextLabel) {
                            /* to be strictly correct, we should be adjusting opts.maxLength to account for the overheads
                          in the format string, and dividing the remainder across all the placeholders in the string,
                          rather than just passing opts on to the child. But that would get complicated, and this is
                          better than nothing... */
                            return block.getTextLabel(opts);
                        }
                        return '';
                    },
                );
            }

            /* if no labelFormat specified, just try each child block in turn until we find one that provides a label */
            for (const childDef of this.blockDef.childBlockDefs) {
                const child = this.childBlocks[childDef.name];
                if (child.getTextLabel) {
                    const val = child.getTextLabel(opts);
                    if (val) return val;
                }
            }
            // no usable label found
            return null;
        }

        focus (opts) {
            if (this.blockDef.childBlockDefs.length) {
                const firstChildName = this.blockDef.childBlockDefs[0].name;
                this.childBlocks[firstChildName].focus(opts);
            }
        }
    }

    class WagtailSBStructBlockDefinition {
        constructor(name, childBlockDefs, meta) {
            this.name = name;
            this.childBlockDefs = childBlockDefs;
            this.meta = meta;
        }

        render (placeholder, prefix, initialState, initialError) {
            return new WagtailSBStructBlock(
                this,
                placeholder,
                prefix,
                initialState,
                initialError,
            );
        }
    }

    window.wagtailStreamField = window.wagtailStreamField || {};

    if (!window.wagtailStreamField.blocks) {
        window.wagtailStreamField.blocks = {};
    }

    window.telepath.register('wagtail_sb_structblock.blocks.structblock', WagtailSBStructBlockDefinition)
})();
