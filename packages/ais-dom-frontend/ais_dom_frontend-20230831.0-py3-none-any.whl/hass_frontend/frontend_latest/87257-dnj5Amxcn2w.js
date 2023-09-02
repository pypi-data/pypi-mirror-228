/*! For license information please see 87257-dnj5Amxcn2w.js.LICENSE.txt */
export const id=87257;export const ids=[87257,66813];export const modules={39841:(t,e,o)=>{o(56299),o(65660);var a=o(9672),r=o(69491),n=o(50856),i=o(44181);(0,a.k)({_template:n.d`
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
`,is:"app-header-layout",behaviors:[i.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,r.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),o=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=o+"px"}.bind(this));var o=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(o.marginTop=e+"px",o.paddingTop=""):(o.paddingTop=e+"px",o.marginTop="")}}})},53973:(t,e,o)=>{o(56299),o(65660),o(97968);var a=o(9672),r=o(50856),n=o(33760);(0,a.k)({_template:r.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[n.U]})},41193:(t,e,o)=>{o.r(e);var a=o(17463),r=(o(27289),o(12730),o(60010),o(27213),o(79932)),n=o(68144);let i=(0,a.Z)(null,(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`.content{padding-bottom:32px}.border{margin:32px auto 0;border-bottom:1px solid rgba(0,0,0,.12);max-width:1040px}.narrow .border{max-width:640px}.center-container{@apply --layout-vertical;@apply --layout-center-center;height:70px}.content{padding-bottom:24px;direction:ltr}.account-row{display:flex;padding:0 16px}mwc-button{align-self:center}.soon{font-style:italic;margin-top:24px;text-align:center}.nowrap{white-space:nowrap}.wrap{white-space:normal}.status{text-transform:capitalize;padding:16px}a{color:var(--primary-color)}.buttons{position:relative;width:200px;height:200px}.button{position:absolute;width:50px;height:50px}.arrow{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}.arrow-up{border-left:12px solid transparent;border-right:12px solid transparent;border-bottom:16px solid #000}.arrow-right{border-top:12px solid transparent;border-bottom:12px solid transparent;border-left:16px solid #000}.arrow-left{border-top:12px solid transparent;border-bottom:12px solid transparent;border-right:16px solid #000}.arrow-down{border-left:12px solid transparent;border-right:12px solid transparent;border-top:16px solid #000}.down{bottom:0;left:75px}.left{top:75px;left:0}.right{top:75px;right:0}.up{top:0;left:75px}div.card-actions{text-align:center}`}},{kind:"method",key:"render",value:function(){return n.dy` <hass-subpage header="Konfiguracja bramki AIS dom"> <div> <ha-config-section .isWide="${this.isWide}"> <span slot="header">Ustawienia ekranu</span> <span slot="introduction">Jeżeli obraz na monitorze lub telewizorze podłączonym do bramki za pomocą złącza HDMI jest ucięty lub przesunięty, to w tym miejscu możesz dostosować obraz do rozmiaru ekranu.</span> <ha-card header="Dostosuj obraz do rozmiaru ekranu"> <div class="card-content"> <div class="card-content" style="text-align:center"> <div style="display:inline-block"> <p>Powiększanie</p> <div class="buttons" style="margin:0 auto;display:table;border:solid 1px"> <button class="button up" data-value="top" @click="${this.wmOverscan}"> <span class="arrow-up arrow"></span> </button> <button class="button down" data-value="bottom" @click="${this.wmOverscan}"> <span class="arrow-down arrow"></span> </button> <button class="button right" data-value="right" @click="${this.wmOverscan}"> <span class="arrow-right arrow"></span> </button> <button class="button left" data-value="left" @click="${this.wmOverscan}"> <span class="arrow-left arrow"></span> </button> </div> </div> <div style="text-align:center;display:inline-block;margin:30px"> <p>Zmniejszanie</p> <div class="buttons" style="margin:0 auto;display:table"> <button class="button up" data-value="-top" @click="${this.wmOverscan}"> <span class="arrow-down arrow"></span> </button> <div style="margin:0 auto;height:98px;width:98px;margin-top:50px;margin-left:50px;display:flex;border:solid 1px"></div> <button class="button down" data-value="-bottom" @click="${this.wmOverscan}"> <span class="arrow-up arrow"></span> </button> <button class="button right" data-value="-right" @click="${this.wmOverscan}"> <span class="arrow-left arrow"></span> </button> <button class="button left" data-value="-left" @click="${this.wmOverscan}"> <span class="arrow-right arrow"></span> </button> </div> </div> </div> <div class="card-actions" style="margin-top:30px"> <mwc-button @click="${this.wmOverscan}" data-value="reset"> <ha-icon class="user-button" icon="mdi:restore"></ha-icon> Reset ekranu do ustawień domyślnych </mwc-button> </div> </div> </ha-card> </ha-config-section> </div> </hass-subpage> `}},{kind:"method",key:"wmOverscan",value:function(t){this.hass.callService("ais_shell_command","change_wm_overscan",{value:t.currentTarget.getAttribute("data-value")})}}]}}),n.oi);customElements.define("ha-config-ais-dom-config-display",i)},82160:(t,e,o)=>{function a(t){return new Promise(((e,o)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>o(t.error)}))}function r(t,e){const o=indexedDB.open(t);o.onupgradeneeded=()=>o.result.createObjectStore(e);const r=a(o);return(t,o)=>r.then((a=>o(a.transaction(e,t).objectStore(e))))}let n;function i(){return n||(n=r("keyval-store","keyval")),n}function s(t,e=i()){return e("readonly",(e=>a(e.get(t))))}function l(t,e,o=i()){return o("readwrite",(o=>(o.put(e,t),a(o.transaction))))}function p(t=i()){return t("readwrite",(t=>(t.clear(),a(t.transaction))))}o.d(e,{MT:()=>r,RV:()=>a,U2:()=>s,ZH:()=>p,t8:()=>l})}};
//# sourceMappingURL=87257-dnj5Amxcn2w.js.map