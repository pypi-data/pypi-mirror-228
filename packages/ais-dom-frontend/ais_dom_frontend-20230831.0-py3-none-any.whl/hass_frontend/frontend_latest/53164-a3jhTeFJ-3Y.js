/*! For license information please see 53164-a3jhTeFJ-3Y.js.LICENSE.txt */
export const id=53164;export const ids=[53164,66813];export const modules={39841:(e,o,t)=>{t(56299),t(65660);var n=t(9672),i=t(69491),a=t(50856),r=t(44181);(0,n.k)({_template:a.d`
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
`,is:"app-header-layout",behaviors:[r.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,i.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var o=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var o=this.getBoundingClientRect(),t=document.documentElement.clientWidth-o.right;e.style.left=o.left+"px",e.style.right=t+"px"}.bind(this));var t=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(t.marginTop=o+"px",t.paddingTop=""):(t.paddingTop=o+"px",t.marginTop="")}}})},53973:(e,o,t)=>{t(56299),t(65660),t(97968);var n=t(9672),i=t(50856),a=t(33760);(0,n.k)({_template:i.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},73728:(e,o,t)=>{t.d(o,{D4:()=>d,D7:()=>u,Ky:()=>c,P3:()=>l,V3:()=>y,WW:()=>v,XO:()=>p,ZJ:()=>m,d4:()=>f,oi:()=>g,pV:()=>r,zO:()=>h});var n=t(97330),i=t(38346),a=t(5986);const r=["bluetooth","dhcp","discovery","hardware","hassio","homekit","integration_discovery","mqtt","ssdp","unignore","usb","zeroconf"],l=["reauth"],s={"HA-Frontend-Base":`${location.protocol}//${location.host}`},c=(e,o)=>{var t;return e.callApi("POST","config/config_entries/flow",{handler:o,show_advanced_options:Boolean(null===(t=e.userData)||void 0===t?void 0:t.showAdvanced)},s)},d=(e,o)=>e.callApi("GET",`config/config_entries/flow/${o}`,void 0,s),p=(e,o,t)=>e.callApi("POST",`config/config_entries/flow/${o}`,t,s),h=(e,o,t)=>e.callWS({type:"config_entries/ignore_flow",flow_id:o,title:t}),g=(e,o)=>e.callApi("DELETE",`config/config_entries/flow/${o}`),f=(e,o)=>e.callApi("GET","config/config_entries/flow_handlers"+(o?`?type=${o}`:"")),u=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),w=(e,o)=>e.subscribeEvents((0,i.D)((()=>u(e).then((e=>o.setState(e,!0)))),500,!0),"config_entry_discovered"),m=e=>(0,n._)(e,"_configFlowProgress",u,w),y=(e,o)=>m(e.connection).subscribe(o),v=(e,o)=>o.context.title_placeholders&&0!==Object.keys(o.context.title_placeholders).length?e(`component.${o.handler}.config.flow_title`,o.context.title_placeholders)||("name"in o.context.title_placeholders?o.context.title_placeholders.name:(0,a.Lh)(e,o.handler)):(0,a.Lh)(e,o.handler)},2852:(e,o,t)=>{t.d(o,{t:()=>l});var n=t(68144),i=t(73728),a=t(5986),r=t(52871);const l=(e,o)=>(0,r.w)(e,o,{flowType:"config_flow",loadDevicesAndAreas:!0,createFlow:async(e,o)=>{const[t]=await Promise.all([(0,i.Ky)(e,o),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config",o),e.loadBackendTranslation("selector",o),e.loadBackendTranslation("title",o)]);return t},fetchFlow:async(e,o)=>{const t=await(0,i.D4)(e,o);return await e.loadFragmentTranslation("config"),await e.loadBackendTranslation("config",t.handler),await e.loadBackendTranslation("selector",t.handler),t},handleFlowStep:i.XO,deleteFlow:i.oi,renderAbortDescription(e,o){const t=e.localize(`component.${o.handler}.config.abort.${o.reason}`,o.description_placeholders);return t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""},renderShowFormStepHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`,o.description_placeholders)||e.localize(`component.${o.handler}.title`),renderShowFormStepDescription(e,o){const t=e.localize(`component.${o.handler}.config.step.${o.step_id}.description`,o.description_placeholders);return t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""},renderShowFormStepFieldLabel:(e,o,t)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.data.${t.name}`),renderShowFormStepFieldHelper(e,o,t){const i=e.localize(`component.${o.handler}.config.step.${o.step_id}.data_description.${t.name}`,o.description_placeholders);return i?n.dy`<ha-markdown breaks .content="${i}"></ha-markdown>`:""},renderShowFormStepFieldError:(e,o,t)=>e.localize(`component.${o.handler}.config.error.${t}`,o.description_placeholders)||t,renderShowFormStepFieldLocalizeValue:(e,o,t)=>e.localize(`component.${o.handler}.selector.${t}`),renderShowFormStepSubmitButton:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===o.last_step?"next":"submit")),renderExternalStepHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,o){const t=e.localize(`component.${o.handler}.config.${o.step_id}.description`,o.description_placeholders);return n.dy` <p> ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")} </p> ${t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""} `},renderCreateEntryDescription(e,o){const t=e.localize(`component.${o.handler}.config.create_entry.${o.description||"default"}`,o.description_placeholders);return n.dy` ${t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""} <p> ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",o.title)} </p> `},renderShowFormProgressHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize(`component.${o.handler}.title`),renderShowFormProgressDescription(e,o){const t=e.localize(`component.${o.handler}.config.progress.${o.progress_action}`,o.description_placeholders);return t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""},renderMenuHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize(`component.${o.handler}.title`),renderMenuDescription(e,o){const t=e.localize(`component.${o.handler}.config.step.${o.step_id}.description`,o.description_placeholders);return t?n.dy` <ha-markdown allowsvg breaks .content="${t}"></ha-markdown> `:""},renderMenuOption:(e,o,t)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.menu_options.${t}`,o.description_placeholders),renderLoadingDescription(e,o,t,n){if("loading_flow"!==o&&"loading_step"!==o)return"";const i=(null==n?void 0:n.handler)||t;return e.localize(`ui.panel.config.integrations.config_flow.loading.${o}`,{integration:i?(0,a.Lh)(e.localize,i):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},52871:(e,o,t)=>{t.d(o,{w:()=>a});var n=t(47181);const i=()=>Promise.all([t.e(46992),t.e(42850),t.e(28426),t.e(28597),t.e(97487),t.e(52154),t.e(90457),t.e(40163),t.e(59159)]).then(t.bind(t,59159)),a=(e,o,t)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:{...o,flowConfig:t,dialogParentElement:e}})}},33137:(e,o,t)=>{t.r(o);var n=t(17463),i=(t(27289),t(12730),t(60010),t(38353),t(27213),t(68144)),a=t(79932),r=t(2852),l=t(47181),s=t(11654);(0,n.Z)([(0,a.Mo)("ha-config-ais-dom-config-wifi")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return this.hass?i.dy` <hass-subpage header="Konfiguracja bramki AIS dom"> <div .narrow="${this.narrow}"> <ha-config-section .isWide="${this.isWide}"> <span slot="header">Połączenie WiFi</span> <span slot="introduction">Możesz sprawdzić lub skonfigurować parametry połączenia WiFi</span> <ha-card header="Parametry sieci"> <div class="card-content" style="display:flex"> <div style="text-align:center"> <div class="aisInfoRow">Lokalna nazwa hosta</div> <div class="aisInfoRow"> <mwc-button>${this.hass.states["sensor.local_host_name"].state} <ha-icon class="user-button" icon="hass:cog" @click="${this.createFlowHostName}"></ha-icon> </mwc-button> </div> </div> <div style="text-align:center" @click="${this.showLocalIpInfo}"> <div class="aisInfoRow">Lokalny adres IP</div> <div class="aisInfoRow"> <mwc-button>${this.hass.states["sensor.internal_ip_address"].state}</mwc-button> </div> </div> <div @click="${this.showWiFiSpeedInfo}" style="text-align:center"> <div class="aisInfoRow">Prędkość połączenia WiFi</div> <div class="aisInfoRow"> <mwc-button>${this.hass.states["sensor.ais_wifi_service_current_network_info"].state}</mwc-button> </div> </div> </div> <div class="card-actions"> <ha-icon class="user-button" icon="hass:wifi" @click="${this.showWiFiGroup}"></ha-icon><mwc-button @click="${this.createFlowWifi}">Konfigurator połączenia z siecą WiFi</mwc-button> </div> </ha-card> </ha-config-section> </div> </hass-subpage> `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`.content{padding-bottom:32px}.border{margin:32px auto 0;border-bottom:1px solid rgba(0,0,0,.12);max-width:1040px}.narrow .border{max-width:640px}div.aisInfoRow{display:inline-block}.center-container{@apply --layout-vertical;@apply --layout-center-center;height:70px}div.card-actions{text-align:center}`]}},{kind:"method",key:"showWiFiGroup",value:function(){(0,l.B)(this,"hass-more-info",{entityId:"group.internet_status"})}},{kind:"method",key:"showWiFiSpeedInfo",value:function(){(0,l.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}},{kind:"method",key:"showLocalIpInfo",value:function(){(0,l.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}},{kind:"method",key:"_continueFlow",value:function(e){(0,r.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}},{kind:"method",key:"createFlowHostName",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}},{kind:"method",key:"createFlowWifi",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}}]}}),i.oi)},82160:(e,o,t)=>{function n(e){return new Promise(((o,t)=>{e.oncomplete=e.onsuccess=()=>o(e.result),e.onabort=e.onerror=()=>t(e.error)}))}function i(e,o){const t=indexedDB.open(e);t.onupgradeneeded=()=>t.result.createObjectStore(o);const i=n(t);return(e,t)=>i.then((n=>t(n.transaction(o,e).objectStore(o))))}let a;function r(){return a||(a=i("keyval-store","keyval")),a}function l(e,o=r()){return o("readonly",(o=>n(o.get(e))))}function s(e,o,t=r()){return t("readwrite",(t=>(t.put(o,e),n(t.transaction))))}function c(e=r()){return e("readwrite",(e=>(e.clear(),n(e.transaction))))}t.d(o,{MT:()=>i,RV:()=>n,U2:()=>l,ZH:()=>c,t8:()=>s})}};
//# sourceMappingURL=53164-a3jhTeFJ-3Y.js.map