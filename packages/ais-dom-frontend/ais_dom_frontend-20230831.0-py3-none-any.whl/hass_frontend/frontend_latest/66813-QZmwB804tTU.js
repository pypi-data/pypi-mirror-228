/*! For license information please see 66813-QZmwB804tTU.js.LICENSE.txt */
export const id=66813;export const ids=[66813];export const modules={39841:(e,t,o)=>{o(56299),o(65660);var i=o(9672),n=o(69491),r=o(50856),a=o(44181);(0,i.k)({_template:r.d`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[a.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,n.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),o=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=o+"px"}.bind(this));var o=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(o.marginTop=t+"px",o.paddingTop=""):(o.paddingTop=t+"px",o.marginTop="")}}})},53973:(e,t,o)=>{o(56299),o(65660),o(97968);var i=o(9672),n=o(50856),r=o(33760);(0,i.k)({_template:n.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[r.U]})},82160:(e,t,o)=>{function i(e){return new Promise(((t,o)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>o(e.error)}))}function n(e,t){const o=indexedDB.open(e);o.onupgradeneeded=()=>o.result.createObjectStore(t);const n=i(o);return(e,o)=>n.then((i=>o(i.transaction(t,e).objectStore(t))))}let r;function a(){return r||(r=n("keyval-store","keyval")),r}function l(e,t=a()){return t("readonly",(t=>i(t.get(e))))}function s(e,t,o=a()){return o("readwrite",(o=>(o.put(t,e),i(o.transaction))))}function p(e=a()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}o.d(t,{MT:()=>n,RV:()=>i,U2:()=>l,ZH:()=>p,t8:()=>s})}};
//# sourceMappingURL=66813-QZmwB804tTU.js.map