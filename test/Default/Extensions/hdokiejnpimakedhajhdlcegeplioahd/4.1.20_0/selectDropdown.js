DropdownInput=function(a,b){DialogInput.ErrorDisplayInput.call(this);this.inputObject=new DialogInput.Input(a);this.shown=!1;this.onChangeCallback=null;this.disabled=!1;this.dropdownEnabled=!0;this.searchValue="";this.clearSearchValueTimeout=null;this.dynamic=!0;this.build(a);this.setOptions(b);var c=this;c.clearSearchValue=function(){c.searchValue=""}};DropdownInput.prototype=Object.create(DialogInput.ErrorDisplayInput.prototype);DropdownInput.prototype.constructor=DropdownInput;
DropdownInput.prototype.ATTR_DROPDOWN_VALUE="dropdownValue";
(function(){DropdownInput.prototype.build=function(a){var b=a.nextElementSibling;null===b&&(b=a.parentElement.nextElementSibling);if(null!==b&&$(b).hasClass("selectDropdownList")){this.dynamic=!1;this.dropdownElement=b;this.options={};this.orderedOptions=[];for(var b=this.dropdownElement.children[0],c=0,f=b.children.length;c<f;++c){var g=b.children[c],d=g.getAttribute(DropdownInput.prototype.ATTR_DROPDOWN_VALUE),g={label:g.textContent.trim(),element:g,value:d,index:c};this.options[d]=g;this.orderedOptions.push(g)}}else this.dropdownElement=
LPTools.createElement("div","dropdownMenu selectDropdownList"),this.dropdownElement.appendChild(LPTools.createElement("ul")),a.parentElement.insertBefore(this.dropdownElement,a.nextElementSibling);$(this.dropdownElement.parentElement).addClass("dropdownContainer");this.$dropdownElement=$(this.dropdownElement);var e=this,h=!1,b=$(a);b.unbind("blur");b.bind("blur",function(){h?(a.focus(),h=!1):e.hide()});b.unbind("keypress");b.bind("keypress",function(a){e.dropdownEnabled&&e.handleKeypress(String.fromCharCode(a.charCode))});
b.unbind("keyup");b.bind("keyup",function(a){if(e.dropdownEnabled)switch(a.keyCode||a.which){case 8:case 46:e.handleDelete()}});b.unbind("keydown");b.bind("keydown",function(a){if(40===(a.keyCode||a.which)&&!1===e.shown)e.handleDownArrow(),a.preventDefault(),a.stopPropagation()});e.toggleHandler=function(a){e.toggle(a)};b.unbind("mousedown");b.bind("mousedown",e.toggleHandler);$(e.dropdownElement.children[0]).unbind("mousedown");$(e.dropdownElement.children[0]).bind("mousedown",function(a){e.setValue(e.getDropdownValue(a.target));
a.stopPropagation();a.preventDefault()});$(e.dropdownElement).unbind("mousedown");$(e.dropdownElement).bind("mousedown",function(a){a.stopPropagation();a.preventDefault();LPPlatform.canPreventBlur()||(h=!0)});$(a).addClass(this.getDropdownClass())};DropdownInput.prototype.enableDropdown=function(){this.dropdownEnabled||(this.getElement().removeClass("dropdownDisabled"),this.dropdownEnabled=!0)};DropdownInput.prototype.disableDropdown=function(){this.dropdownEnabled&&(this.getElement().addClass("dropdownDisabled"),
this.dropdownEnabled=!1)};DropdownInput.prototype.getElement=function(){return this.inputObject.getElement()};DropdownInput.prototype.buildError=function(a){return LPTools.buildErrorElement({collection:this.getElement(),dialog:a,alignTop:!0})};DropdownInput.prototype.validate=function(){return!0};DropdownInput.prototype.getDropdownClass=function(){return"selectDropdown"};DropdownInput.prototype.setValues=function(a){var b=[];if(a)for(var c=0,f=a.length;c<f;++c){var g=a[c];b.push({value:g,label:g})}this.setOptions(b)};
DropdownInput.prototype.default=function(){};DropdownInput.prototype.addOption=function(a){this.options[a.value]=a};DropdownInput.prototype.setOptions=function(a,b){if(a){this.options={};this.orderedOptions=[];var c=this.dropdownElement.children[0];LPTools.removeDOMChildren(c);for(var f=0,g=a.length;f<g;++f){var d=a[f];d.index=f;void 0===d.element?d.element=LPTools.createElement("li",{dropdownValue:d.value},d.label):d.element.setAttribute(this.ATTR_DROPDOWN_VALUE,d.value);b&&(d.element.className=
b);"undefined"!==typeof d.click&&LPPlatform.addEventListener(d.element,"mousedown",d.click);c.appendChild(d.element);this.options[d.value]=d;this.orderedOptions.push(d)}}};DropdownInput.prototype.focus=function(){this.getElement().focus()};DropdownInput.prototype.onChange=function(a){this.onChangeCallback=a};DropdownInput.prototype.fireOnChange=function(a){if(null!==this.onChangeCallback)this.onChangeCallback(a)};DropdownInput.prototype.getDropdownValue=function(a){for(;a&&a!==this.dropdownElement;){var b=
a.getAttribute(DropdownInput.prototype.ATTR_DROPDOWN_VALUE);if(null!==b)return b;a=a.parentElement}return null};DropdownInput.prototype.addKeyBoardNavigation=function(){LPTools.addKeyBoardNavigation(this.dropdownElement.children[0].children,{mouseEvent:"mousedown",useRightArrow:!1})};DropdownInput.prototype.show=function(a){!this.disabled&&(this.dropdownEnabled&&!this.shown&&LPTools.hasProperties(this.options))&&(this.shown=!0,this.inputObject.getElement().addClass("toggled"),this.addKeyBoardNavigation(),
this.$dropdownElement.show(),this.dropdownElement.scrollTop=0,void 0!==a&&a.stopPropagation())};DropdownInput.prototype.hide=function(){this.shown&&LPTools.hasProperties(this.options)&&(this.shown=!1,LPTools.removeKeyBoardNavigation(),this.$dropdownElement.hide(),this.inputObject.getElement().removeClass("toggled"))};DropdownInput.prototype.toggle=function(a){this.shown?this.hide():this.show();void 0!==a&&a.stopPropagation()};DropdownInput.prototype.disable=function(){this.disabled||(this.getElement().parent().append(LPTools.createElement("div",
"dialogInputOverlay")),this.inputObject.disable(),this.disabled=!0)};DropdownInput.prototype.enable=function(){this.disabled&&(this.getElement().parent().children().last().remove(),this.inputObject.enable(),this.disabled=!1)};DropdownInput.prototype.setReadOnly=function(){this.getElement().prop("readonly",!0)};DropdownInput.prototype.removeReadOnly=function(){this.getElement().prop("readonly",!0)};DropdownInput.prototype.getValue=function(){var a=this.inputObject.getValue();if(this.dropdownEnabled&&
this.options)for(var b in this.options)if(a===this.options[b].label){a=b;break}return a};DropdownInput.prototype.getInputValue=function(a){return a.label};DropdownInput.prototype.clear=function(){DialogInput.ErrorDisplayInput.prototype.clear.apply(this,arguments);this.setValue("")};DropdownInput.prototype.setValue=function(a){if(this.dropdownEnabled&&this.options&&this.options[a]){var b=this.options[a];this.inputObject.setValue(this.getInputValue(b));this.optionIndex=b.index}else this.inputObject.setValue(a);
this.hide();this.fireOnChange(a)};DropdownInput.prototype.handleKeypress=function(a){this.searchValue+=a;this.updateValue(this.searchValue);this.clearSearchValueTimeout&&clearTimeout(this.clearSearchValueTimeout);var b=this.clearSearchValue;this.clearSearchValueTimeout=setTimeout(function(){b()},500)};DropdownInput.prototype.handleDelete=function(){this.searchValue="";this.updateValue(this.searchValue)};DropdownInput.prototype.handleDownArrow=function(){this.show();LPTools.setNavIndex(this.optionIndex)};
DropdownInput.prototype.queryMatches=function(a,b,c){a=a.label.toLowerCase();b=b.toLowerCase();b=a.indexOf(b);return c?-1<b:0===b};DropdownInput.prototype.updateValue=function(a){for(var b=0,c=this.orderedOptions.length;b<c;++b){var f=this.orderedOptions[b];if(this.queryMatches(f,a)){this.setValue(f.value);break}}}})(document);
