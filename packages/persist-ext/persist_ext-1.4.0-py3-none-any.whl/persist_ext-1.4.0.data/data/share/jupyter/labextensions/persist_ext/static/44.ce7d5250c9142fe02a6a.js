/*! For license information please see 44.ce7d5250c9142fe02a6a.js.LICENSE.txt */
"use strict";(self.webpackChunkpersist_ext=self.webpackChunkpersist_ext||[]).push([[44],{44:(e,t,n)=>{Object.defineProperty(t,"__esModule",{value:!0});var o=n(6029),a=n(3595);function l(e){return e&&"object"==typeof e&&"default"in e?e:{default:e}}var r,i=function(e){if(e&&e.__esModule)return e;var t=Object.create(null);return e&&Object.keys(e).forEach((function(n){if("default"!==n){var o=Object.getOwnPropertyDescriptor(e,n);Object.defineProperty(t,n,o.get?o:{enumerable:!0,get:function(){return e[n]}})}})),t.default=e,Object.freeze(t)}(o),s=l(o),d=l(a);function c(e,t){return e[t]}function g(e,t){return t.split(".").reduce(((e,t)=>{const n=t.match(/[^\]\\[.]+/g);if(n&&n.length>1)for(let t=0;t<n.length;t++)return e[n[t]][n[t+1]];return e[t]}),e)}function u(e=[],t,n=0){return[...e.slice(0,n),t,...e.slice(n)]}function p(e=[],t,n="id"){const o=e.slice(),a=c(t,n);return a?o.splice(o.findIndex((e=>c(e,n)===a)),1):o.splice(o.findIndex((e=>e===t)),1),o}function b(e){return e.map(((e,t)=>{const n=Object.assign(Object.assign({},e),{sortable:e.sortable||!!e.sortFunction||void 0});return e.id||(n.id=t+1),n}))}function f(e,t){return Math.ceil(e/t)}function m(e,t){return Math.min(e,t)}!function(e){e.ASC="asc",e.DESC="desc"}(r||(r={}));const h=()=>null;function w(e,t=[],n=[]){let o={},a=[...n];return t.length&&t.forEach((t=>{if(!t.when||"function"!=typeof t.when)throw new Error('"when" must be defined in the conditional style object and must be function');t.when(e)&&(o=t.style||{},t.classNames&&(a=[...a,...t.classNames]),"function"==typeof t.style&&(o=t.style(e)||{}))})),{style:o,classNames:a.join(" ")}}function x(e,t=[],n="id"){const o=c(e,n);return o?t.some((e=>c(e,n)===o)):t.some((t=>t===e))}function C(e,t){return t?e.findIndex((e=>y(e.id,t))):-1}function y(e,t){return e==t}function v(e,t){const n=!e.toggleOnSelectedRowsChange;switch(t.type){case"SELECT_ALL_ROWS":{const{keyField:n,rows:o,rowCount:a,mergeSelections:l}=t,r=!e.allSelected,i=!e.toggleOnSelectedRowsChange;if(l){const t=r?[...e.selectedRows,...o.filter((t=>!x(t,e.selectedRows,n)))]:e.selectedRows.filter((e=>!x(e,o,n)));return Object.assign(Object.assign({},e),{allSelected:r,selectedCount:t.length,selectedRows:t,toggleOnSelectedRowsChange:i})}return Object.assign(Object.assign({},e),{allSelected:r,selectedCount:r?a:0,selectedRows:r?o:[],toggleOnSelectedRowsChange:i})}case"SELECT_SINGLE_ROW":{const{keyField:o,row:a,isSelected:l,rowCount:r,singleSelect:i}=t;return i?l?Object.assign(Object.assign({},e),{selectedCount:0,allSelected:!1,selectedRows:[],toggleOnSelectedRowsChange:n}):Object.assign(Object.assign({},e),{selectedCount:1,allSelected:!1,selectedRows:[a],toggleOnSelectedRowsChange:n}):l?Object.assign(Object.assign({},e),{selectedCount:e.selectedRows.length>0?e.selectedRows.length-1:0,allSelected:!1,selectedRows:p(e.selectedRows,a,o),toggleOnSelectedRowsChange:n}):Object.assign(Object.assign({},e),{selectedCount:e.selectedRows.length+1,allSelected:e.selectedRows.length+1===r,selectedRows:u(e.selectedRows,a),toggleOnSelectedRowsChange:n})}case"SELECT_MULTIPLE_ROWS":{const{keyField:o,selectedRows:a,totalRows:l,mergeSelections:r}=t;if(r){const t=[...e.selectedRows,...a.filter((t=>!x(t,e.selectedRows,o)))];return Object.assign(Object.assign({},e),{selectedCount:t.length,allSelected:!1,selectedRows:t,toggleOnSelectedRowsChange:n})}return Object.assign(Object.assign({},e),{selectedCount:a.length,allSelected:a.length===l,selectedRows:a,toggleOnSelectedRowsChange:n})}case"CLEAR_SELECTED_ROWS":{const{selectedRowsFlag:n}=t;return Object.assign(Object.assign({},e),{allSelected:!1,selectedCount:0,selectedRows:[],selectedRowsFlag:n})}case"SORT_CHANGE":{const{sortDirection:o,selectedColumn:a,clearSelectedOnSort:l}=t;return Object.assign(Object.assign(Object.assign({},e),{selectedColumn:a,sortDirection:o,currentPage:1}),l&&{allSelected:!1,selectedCount:0,selectedRows:[],toggleOnSelectedRowsChange:n})}case"CHANGE_PAGE":{const{page:o,paginationServer:a,visibleOnly:l,persistSelectedOnPageChange:r}=t,i=a&&r,s=a&&!r||l;return Object.assign(Object.assign(Object.assign(Object.assign({},e),{currentPage:o}),i&&{allSelected:!1}),s&&{allSelected:!1,selectedCount:0,selectedRows:[],toggleOnSelectedRowsChange:n})}case"CHANGE_ROWS_PER_PAGE":{const{rowsPerPage:n,page:o}=t;return Object.assign(Object.assign({},e),{currentPage:o,rowsPerPage:n})}}}const R=a.css`
	pointer-events: none;
	opacity: 0.4;
`,S=d.default.div`
	position: relative;
	box-sizing: border-box;
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
	max-width: 100%;
	${({disabled:e})=>e&&R};
	${({theme:e})=>e.table.style};
`,E=a.css`
	position: sticky;
	position: -webkit-sticky; /* Safari */
	top: 0;
	z-index: 1;
`,O=d.default.div`
	display: flex;
	width: 100%;
	${({$fixedHeader:e})=>e&&E};
	${({theme:e})=>e.head.style};
`,$=d.default.div`
	display: flex;
	align-items: stretch;
	width: 100%;
	${({theme:e})=>e.headRow.style};
	${({$dense:e,theme:t})=>e&&t.headRow.denseStyle};
`,P=(e,...t)=>a.css`
		@media screen and (max-width: ${599}px) {
			${a.css(e,...t)}
		}
	`,k=(e,...t)=>a.css`
		@media screen and (max-width: ${959}px) {
			${a.css(e,...t)}
		}
	`,D=(e,...t)=>a.css`
		@media screen and (max-width: ${1280}px) {
			${a.css(e,...t)}
		}
	`,H=d.default.div`
	position: relative;
	display: flex;
	align-items: center;
	box-sizing: border-box;
	line-height: normal;
	${({theme:e,$headCell:t})=>e[t?"headCells":"cells"].style};
	${({$noPadding:e})=>e&&"padding: 0"};
`,j=d.default(H)`
	flex-grow: ${({button:e,grow:t})=>0===t||e?0:t||1};
	flex-shrink: 0;
	flex-basis: 0;
	max-width: ${({maxWidth:e})=>e||"100%"};
	min-width: ${({minWidth:e})=>e||"100px"};
	${({width:e})=>e&&a.css`
			min-width: ${e};
			max-width: ${e};
		`};
	${({right:e})=>e&&"justify-content: flex-end"};
	${({button:e,center:t})=>(t||e)&&"justify-content: center"};
	${({compact:e,button:t})=>(e||t)&&"padding: 0"};

	/* handle hiding cells */
	${({hide:e})=>e&&"sm"===e&&P`
    display: none;
  `};
	${({hide:e})=>e&&"md"===e&&k`
    display: none;
  `};
	${({hide:e})=>e&&"lg"===e&&D`
    display: none;
  `};
	${({hide:e})=>e&&Number.isInteger(e)&&(e=>(t,...n)=>a.css`
				@media screen and (max-width: ${e}px) {
					${a.css(t,...n)}
				}
			`)(e)`
    display: none;
  `};
`,F=a.css`
	div:first-child {
		white-space: ${({$wrapCell:e})=>e?"normal":"nowrap"};
		overflow: ${({$allowOverflow:e})=>e?"visible":"hidden"};
		text-overflow: ellipsis;
	}
`,T=d.default(j).attrs((e=>({style:e.style})))`
	${({$renderAsCell:e})=>!e&&F};
	${({theme:e,$isDragging:t})=>t&&e.cells.draggingStyle};
	${({$cellStyle:e})=>e};
`;var I=i.memo((function({id:e,column:t,row:n,rowIndex:o,dataTag:a,isDragging:l,onDragStart:r,onDragOver:s,onDragEnd:d,onDragEnter:c,onDragLeave:u}){const{style:p,classNames:b}=w(n,t.conditionalCellStyles,["rdt_TableCell"]);return i.createElement(T,{id:e,"data-column-id":t.id,role:"cell",className:b,"data-tag":a,$cellStyle:t.style,$renderAsCell:!!t.cell,$allowOverflow:t.allowOverflow,button:t.button,center:t.center,compact:t.compact,grow:t.grow,hide:t.hide,maxWidth:t.maxWidth,minWidth:t.minWidth,right:t.right,width:t.width,$wrapCell:t.wrap,style:p,$isDragging:l,onDragStart:r,onDragOver:s,onDragEnd:d,onDragEnter:c,onDragLeave:u},!t.cell&&i.createElement("div",{"data-tag":a},function(e,t,n,o){if(!t)return null;if("string"!=typeof t&&"function"!=typeof t)throw new Error("selector must be a . delimited string eg (my.property) or function (e.g. row => row.field");return n&&"function"==typeof n?n(e,o):t&&"function"==typeof t?t(e,o):g(e,t)}(n,t.selector,t.format,o)),t.cell&&t.cell(n,o,t,e))})),M=i.memo((function({name:e,component:t="input",componentOptions:n={style:{}},indeterminate:o=!1,checked:a=!1,disabled:l=!1,onClick:r=h}){const s=t,d="input"!==s?n.style:(e=>Object.assign(Object.assign({fontSize:"18px"},!e&&{cursor:"pointer"}),{padding:0,marginTop:"1px",verticalAlign:"middle",position:"relative"}))(l),c=i.useMemo((()=>function(e,...t){let n;return Object.keys(e).map((t=>e[t])).forEach(((o,a)=>{const l=e;"function"==typeof o&&(n=Object.assign(Object.assign({},l),{[Object.keys(e)[a]]:o(...t)}))})),n||e}(n,o)),[n,o]);return i.createElement(s,Object.assign({type:"checkbox",ref:e=>{e&&(e.indeterminate=o)},style:d,onClick:l?h:r,name:e,"aria-label":e,checked:a,disabled:l},c,{onChange:h}))}));const A=d.default(H)`
	flex: 0 0 48px;
	min-width: 48px;
	justify-content: center;
	align-items: center;
	user-select: none;
	white-space: nowrap;
`;function L({name:e,keyField:t,row:n,rowCount:o,selected:a,selectableRowsComponent:l,selectableRowsComponentProps:r,selectableRowsSingle:s,selectableRowDisabled:d,onSelectedRow:c}){const g=!(!d||!d(n));return i.createElement(A,{onClick:e=>e.stopPropagation(),className:"rdt_TableCell",$noPadding:!0},i.createElement(M,{name:e,component:l,componentOptions:r,checked:a,"aria-checked":a,onClick:()=>{c({type:"SELECT_SINGLE_ROW",row:n,isSelected:a,keyField:t,rowCount:o,singleSelect:s})},disabled:g}))}const _=d.default.button`
	display: inline-flex;
	align-items: center;
	user-select: none;
	white-space: nowrap;
	border: none;
	background-color: transparent;
	${({theme:e})=>e.expanderButton.style};
`;function z({disabled:e=!1,expanded:t=!1,expandableIcon:n,id:o,row:a,onToggled:l}){const r=t?n.expanded:n.collapsed;return i.createElement(_,{"aria-disabled":e,onClick:()=>l&&l(a),"data-testid":`expander-button-${o}`,disabled:e,"aria-label":t?"Collapse Row":"Expand Row",role:"button",type:"button"},r)}const N=d.default(H)`
	white-space: nowrap;
	font-weight: 400;
	min-width: 48px;
	${({theme:e})=>e.expanderCell.style};
`;function W({row:e,expanded:t=!1,expandableIcon:n,id:o,onToggled:a,disabled:l=!1}){return i.createElement(N,{onClick:e=>e.stopPropagation(),$noPadding:!0},i.createElement(z,{id:o,row:e,expanded:t,expandableIcon:n,disabled:l,onToggled:a}))}const B=d.default.div`
	width: 100%;
	box-sizing: border-box;
	${({theme:e})=>e.expanderRow.style};
	${({$extendedRowStyle:e})=>e};
`;var G,V,U,Y=i.memo((function({data:e,ExpanderComponent:t,expanderComponentProps:n,extendedRowStyle:o,extendedClassNames:a}){const l=["rdt_ExpanderRow",...a.split(" ").filter((e=>"rdt_TableRow"!==e))].join(" ");return i.createElement(B,{className:l,$extendedRowStyle:o},i.createElement(t,Object.assign({data:e},n)))}));t.Direction=void 0,(G=t.Direction||(t.Direction={})).LTR="ltr",G.RTL="rtl",G.AUTO="auto",t.Alignment=void 0,(V=t.Alignment||(t.Alignment={})).LEFT="left",V.RIGHT="right",V.CENTER="center",t.Media=void 0,(U=t.Media||(t.Media={})).SM="sm",U.MD="md",U.LG="lg";const K=a.css`
	&:hover {
		${({$highlightOnHover:e,theme:t})=>e&&t.rows.highlightOnHoverStyle};
	}
`,q=a.css`
	&:hover {
		cursor: pointer;
	}
`,J=d.default.div.attrs((e=>({style:e.style})))`
	display: flex;
	align-items: stretch;
	align-content: stretch;
	width: 100%;
	box-sizing: border-box;
	${({theme:e})=>e.rows.style};
	${({$dense:e,theme:t})=>e&&t.rows.denseStyle};
	${({$striped:e,theme:t})=>e&&t.rows.stripedStyle};
	${({$highlightOnHover:e})=>e&&K};
	${({$pointerOnHover:e})=>e&&q};
	${({$selected:e,theme:t})=>e&&t.rows.selectedHighlightStyle};
`;function Q({columns:e=[],conditionalRowStyles:t=[],defaultExpanded:n=!1,defaultExpanderDisabled:o=!1,dense:a=!1,expandableIcon:l,expandableRows:r=!1,expandableRowsComponent:s,expandableRowsComponentProps:d,expandableRowsHideExpander:g,expandOnRowClicked:u=!1,expandOnRowDoubleClicked:p=!1,highlightOnHover:b=!1,id:f,expandableInheritConditionalStyles:m,keyField:x,onRowClicked:C=h,onRowDoubleClicked:v=h,onRowMouseEnter:R=h,onRowMouseLeave:S=h,onRowExpandToggled:E=h,onSelectedRow:O=h,pointerOnHover:$=!1,row:P,rowCount:k,rowIndex:D,selectableRowDisabled:H=null,selectableRows:j=!1,selectableRowsComponent:F,selectableRowsComponentProps:T,selectableRowsHighlight:M=!1,selectableRowsSingle:A=!1,selected:_,striped:z=!1,draggingColumnId:N,onDragStart:B,onDragOver:G,onDragEnd:V,onDragEnter:U,onDragLeave:K}){const[q,Q]=i.useState(n);i.useEffect((()=>{Q(n)}),[n]);const X=i.useCallback((()=>{Q(!q),E(!q,P)}),[q,E,P]),Z=$||r&&(u||p),ee=i.useCallback((e=>{e.target&&"allowRowEvents"===e.target.getAttribute("data-tag")&&(C(P,e),!o&&r&&u&&X())}),[o,u,r,X,C,P]),te=i.useCallback((e=>{e.target&&"allowRowEvents"===e.target.getAttribute("data-tag")&&(v(P,e),!o&&r&&p&&X())}),[o,p,r,X,v,P]),ne=i.useCallback((e=>{R(P,e)}),[R,P]),oe=i.useCallback((e=>{S(P,e)}),[S,P]),ae=c(P,x),{style:le,classNames:re}=w(P,t,["rdt_TableRow"]),ie=M&&_,se=m?le:{},de=z&&D%2==0;return i.createElement(i.Fragment,null,i.createElement(J,{id:`row-${f}`,role:"row",$striped:de,$highlightOnHover:b,$pointerOnHover:!o&&Z,$dense:a,onClick:ee,onDoubleClick:te,onMouseEnter:ne,onMouseLeave:oe,className:re,$selected:ie,style:le},j&&i.createElement(L,{name:`select-row-${ae}`,keyField:x,row:P,rowCount:k,selected:_,selectableRowsComponent:F,selectableRowsComponentProps:T,selectableRowDisabled:H,selectableRowsSingle:A,onSelectedRow:O}),r&&!g&&i.createElement(W,{id:ae,expandableIcon:l,expanded:q,row:P,onToggled:X,disabled:o}),e.map((e=>e.omit?null:i.createElement(I,{id:`cell-${e.id}-${ae}`,key:`cell-${e.id}-${ae}`,dataTag:e.ignoreRowClick||e.button?null:"allowRowEvents",column:e,row:P,rowIndex:D,isDragging:y(N,e.id),onDragStart:B,onDragOver:G,onDragEnd:V,onDragEnter:U,onDragLeave:K})))),r&&q&&i.createElement(Y,{key:`expander-${ae}`,data:P,extendedRowStyle:se,extendedClassNames:re,ExpanderComponent:s,expanderComponentProps:d}))}const X=d.default.span`
	padding: 2px;
	color: inherit;
	flex-grow: 0;
	flex-shrink: 0;
	${({$sortActive:e})=>e?"opacity: 1":"opacity: 0"};
	${({$sortDirection:e})=>"desc"===e&&"transform: rotate(180deg)"};
`,Z=({sortActive:e,sortDirection:t})=>s.default.createElement(X,{$sortActive:e,$sortDirection:t},"▲"),ee=d.default(j)`
	${({button:e})=>e&&"text-align: center"};
	${({theme:e,$isDragging:t})=>t&&e.headCells.draggingStyle};
`,te=a.css`
	cursor: pointer;
	span.__rdt_custom_sort_icon__ {
		i,
		svg {
			transform: 'translate3d(0, 0, 0)';
			${({sortActive:e})=>e?"opacity: 1":"opacity: 0"};
			color: inherit;
			font-size: 18px;
			height: 18px;
			width: 18px;
			backface-visibility: hidden;
			transform-style: preserve-3d;
			transition-duration: 95ms;
			transition-property: transform;
		}

		&.asc i,
		&.asc svg {
			transform: rotate(180deg);
		}
	}

	${({sortActive:e})=>!e&&a.css`
			&:hover,
			&:focus {
				opacity: 0.7;

				span,
				span.__rdt_custom_sort_icon__ * {
					opacity: 0.7;
				}
			}
		`};
`,ne=d.default.div`
	display: inline-flex;
	align-items: center;
	justify-content: inherit;
	height: 100%;
	width: 100%;
	outline: none;
	user-select: none;
	overflow: hidden;
	${({disabled:e})=>!e&&te};
`,oe=d.default.div`
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
`;var ae=i.memo((function({column:e,disabled:t,draggingColumnId:n,selectedColumn:o={},sortDirection:a,sortIcon:l,sortServer:s,pagination:d,paginationServer:c,persistSelectedOnSort:g,selectableRowsVisibleOnly:u,onSort:p,onDragStart:b,onDragOver:f,onDragEnd:m,onDragEnter:h,onDragLeave:w}){i.useEffect((()=>{"string"==typeof e.selector&&console.error(`Warning: ${e.selector} is a string based column selector which has been deprecated as of v7 and will be removed in v8. Instead, use a selector function e.g. row => row[field]...`)}),[]);const[x,C]=i.useState(!1),v=i.useRef(null);if(i.useEffect((()=>{v.current&&C(v.current.scrollWidth>v.current.clientWidth)}),[x]),e.omit)return null;const R=()=>{if(!e.sortable&&!e.selector)return;let t=a;y(o.id,e.id)&&(t=a===r.ASC?r.DESC:r.ASC),p({type:"SORT_CHANGE",sortDirection:t,selectedColumn:e,clearSelectedOnSort:d&&c&&!g||s||u})},S=e=>i.createElement(Z,{sortActive:e,sortDirection:a}),E=()=>i.createElement("span",{className:[a,"__rdt_custom_sort_icon__"].join(" ")},l),O=!(!e.sortable||!y(o.id,e.id)),$=!e.sortable||t,P=e.sortable&&!l&&!e.right,k=e.sortable&&!l&&e.right,D=e.sortable&&l&&!e.right,H=e.sortable&&l&&e.right;return i.createElement(ee,{"data-column-id":e.id,className:"rdt_TableCol",$headCell:!0,allowOverflow:e.allowOverflow,button:e.button,compact:e.compact,grow:e.grow,hide:e.hide,maxWidth:e.maxWidth,minWidth:e.minWidth,right:e.right,center:e.center,width:e.width,draggable:e.reorder,$isDragging:y(e.id,n),onDragStart:b,onDragOver:f,onDragEnd:m,onDragEnter:h,onDragLeave:w},e.name&&i.createElement(ne,{"data-column-id":e.id,"data-sort-id":e.id,role:"columnheader",tabIndex:0,className:"rdt_TableCol_Sortable",onClick:$?void 0:R,onKeyPress:$?void 0:e=>{"Enter"===e.key&&R()},sortActive:!$&&O,disabled:$},!$&&H&&E(),!$&&k&&S(O),"string"==typeof e.name?i.createElement(oe,{title:x?e.name:void 0,ref:v,"data-column-id":e.id},e.name):e.name,!$&&D&&E(),!$&&P&&S(O)))}));const le=d.default(H)`
	flex: 0 0 48px;
	justify-content: center;
	align-items: center;
	user-select: none;
	white-space: nowrap;
	font-size: unset;
`;function re({headCell:e=!0,rowData:t,keyField:n,allSelected:o,mergeSelections:a,selectedRows:l,selectableRowsComponent:r,selectableRowsComponentProps:s,selectableRowDisabled:d,onSelectAllRows:c}){const g=l.length>0&&!o,u=d?t.filter((e=>!d(e))):t,p=0===u.length,b=Math.min(t.length,u.length);return i.createElement(le,{className:"rdt_TableCol",$headCell:e,$noPadding:!0},i.createElement(M,{name:"select-all-rows",component:r,componentOptions:s,onClick:()=>{c({type:"SELECT_ALL_ROWS",rows:u,rowCount:b,mergeSelections:a,keyField:n})},checked:o,indeterminate:g,disabled:p}))}function ie(e=t.Direction.AUTO){const n="object"==typeof window,[o,a]=i.useState(!1);return i.useEffect((()=>{if(n)if("auto"!==e)a("rtl"===e);else{const e=!(!window.document||!window.document.createElement),t=document.getElementsByTagName("BODY")[0],n=document.getElementsByTagName("HTML")[0],o="rtl"===t.dir||"rtl"===n.dir;a(e&&o)}}),[e,n]),o}const se=d.default.div`
	display: flex;
	align-items: center;
	flex: 1 0 auto;
	height: 100%;
	color: ${({theme:e})=>e.contextMenu.fontColor};
	font-size: ${({theme:e})=>e.contextMenu.fontSize};
	font-weight: 400;
`,de=d.default.div`
	display: flex;
	align-items: center;
	justify-content: flex-end;
	flex-wrap: wrap;
`,ce=d.default.div`
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	box-sizing: inherit;
	z-index: 1;
	align-items: center;
	justify-content: space-between;
	display: flex;
	${({$rtl:e})=>e&&"direction: rtl"};
	${({theme:e})=>e.contextMenu.style};
	${({theme:e,$visible:t})=>t&&e.contextMenu.activeStyle};
`;function ge({contextMessage:e,contextActions:t,contextComponent:n,selectedCount:o,direction:a}){const l=ie(a),r=o>0;return n?i.createElement(ce,{$visible:r},i.cloneElement(n,{selectedCount:o})):i.createElement(ce,{$visible:r,$rtl:l},i.createElement(se,null,((e,t,n)=>{if(0===t)return null;const o=1===t?e.singular:e.plural;return n?`${t} ${e.message||""} ${o}`:`${t} ${o} ${e.message||""}`})(e,o,l)),i.createElement(de,null,t))}const ue=d.default.div`
	position: relative;
	box-sizing: border-box;
	overflow: hidden;
	display: flex;
	flex: 1 1 auto;
	align-items: center;
	justify-content: space-between;
	width: 100%;
	flex-wrap: wrap;
	${({theme:e})=>e.header.style}
`,pe=d.default.div`
	flex: 1 0 auto;
	color: ${({theme:e})=>e.header.fontColor};
	font-size: ${({theme:e})=>e.header.fontSize};
	font-weight: 400;
`,be=d.default.div`
	flex: 1 0 auto;
	display: flex;
	align-items: center;
	justify-content: flex-end;

	> * {
		margin-left: 5px;
	}
`,fe=({title:e,actions:t=null,contextMessage:n,contextActions:o,contextComponent:a,selectedCount:l,direction:r,showMenu:s=!0})=>i.createElement(ue,{className:"rdt_TableHeader",role:"heading","aria-level":1},i.createElement(pe,null,e),t&&i.createElement(be,null,t),s&&i.createElement(ge,{contextMessage:n,contextActions:o,contextComponent:a,direction:r,selectedCount:l}));function me(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var a=0;for(o=Object.getOwnPropertySymbols(e);a<o.length;a++)t.indexOf(o[a])<0&&Object.prototype.propertyIsEnumerable.call(e,o[a])&&(n[o[a]]=e[o[a]])}return n}const he={left:"flex-start",right:"flex-end",center:"center"},we=d.default.header`
	position: relative;
	display: flex;
	flex: 1 1 auto;
	box-sizing: border-box;
	align-items: center;
	padding: 4px 16px 4px 24px;
	width: 100%;
	justify-content: ${({align:e})=>he[e]};
	flex-wrap: ${({$wrapContent:e})=>e?"wrap":"nowrap"};
	${({theme:e})=>e.subHeader.style}
`,xe=e=>{var{align:t="right",wrapContent:n=!0}=e,o=me(e,["align","wrapContent"]);return i.createElement(we,Object.assign({align:t,$wrapContent:n},o))},Ce=d.default.div`
	display: flex;
	flex-direction: column;
`,ye=d.default.div`
	position: relative;
	width: 100%;
	border-radius: inherit;
	${({$responsive:e,$fixedHeader:t})=>e&&a.css`
			overflow-x: auto;

			// hidden prevents vertical scrolling in firefox when fixedHeader is disabled
			overflow-y: ${t?"auto":"hidden"};
			min-height: 0;
		`};

	${({$fixedHeader:e=!1,$fixedHeaderScrollHeight:t="100vh"})=>e&&a.css`
			max-height: ${t};
			-webkit-overflow-scrolling: touch;
		`};

	${({theme:e})=>e.responsiveWrapper.style};
`,ve=d.default.div`
	position: relative;
	box-sizing: border-box;
	width: 100%;
	height: 100%;
	${e=>e.theme.progress.style};
`,Re=d.default.div`
	position: relative;
	width: 100%;
	${({theme:e})=>e.tableWrapper.style};
`,Se=d.default(H)`
	white-space: nowrap;
	${({theme:e})=>e.expanderCell.style};
`,Ee=d.default.div`
	box-sizing: border-box;
	width: 100%;
	height: 100%;
	${({theme:e})=>e.noData.style};
`,Oe=()=>s.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24"},s.default.createElement("path",{d:"M7 10l5 5 5-5z"}),s.default.createElement("path",{d:"M0 0h24v24H0z",fill:"none"})),$e=d.default.select`
	cursor: pointer;
	height: 24px;
	max-width: 100%;
	user-select: none;
	padding-left: 8px;
	padding-right: 24px;
	box-sizing: content-box;
	font-size: inherit;
	color: inherit;
	border: none;
	background-color: transparent;
	appearance: none;
	direction: ltr;
	flex-shrink: 0;

	&::-ms-expand {
		display: none;
	}

	&:disabled::-ms-expand {
		background: #f60;
	}

	option {
		color: initial;
	}
`,Pe=d.default.div`
	position: relative;
	flex-shrink: 0;
	font-size: inherit;
	color: inherit;
	margin-top: 1px;

	svg {
		top: 0;
		right: 0;
		color: inherit;
		position: absolute;
		fill: currentColor;
		width: 24px;
		height: 24px;
		display: inline-block;
		user-select: none;
		pointer-events: none;
	}
`,ke=e=>{var{defaultValue:t,onChange:n}=e,o=me(e,["defaultValue","onChange"]);return i.createElement(Pe,null,i.createElement($e,Object.assign({onChange:n,defaultValue:t},o)),i.createElement(Oe,null))},De={columns:[],data:[],title:"",keyField:"id",selectableRows:!1,selectableRowsHighlight:!1,selectableRowsNoSelectAll:!1,selectableRowSelected:null,selectableRowDisabled:null,selectableRowsComponent:"input",selectableRowsComponentProps:{},selectableRowsVisibleOnly:!1,selectableRowsSingle:!1,clearSelectedRows:!1,expandableRows:!1,expandableRowDisabled:null,expandableRowExpanded:null,expandOnRowClicked:!1,expandableRowsHideExpander:!1,expandOnRowDoubleClicked:!1,expandableInheritConditionalStyles:!1,expandableRowsComponent:function(){return s.default.createElement("div",null,"To add an expander pass in a component instance via ",s.default.createElement("strong",null,"expandableRowsComponent"),". You can then access props.data from this component.")},expandableIcon:{collapsed:s.default.createElement((()=>s.default.createElement("svg",{fill:"currentColor",height:"24",viewBox:"0 0 24 24",width:"24",xmlns:"http://www.w3.org/2000/svg"},s.default.createElement("path",{d:"M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z"}),s.default.createElement("path",{d:"M0-.25h24v24H0z",fill:"none"}))),null),expanded:s.default.createElement((()=>s.default.createElement("svg",{fill:"currentColor",height:"24",viewBox:"0 0 24 24",width:"24",xmlns:"http://www.w3.org/2000/svg"},s.default.createElement("path",{d:"M7.41 7.84L12 12.42l4.59-4.58L18 9.25l-6 6-6-6z"}),s.default.createElement("path",{d:"M0-.75h24v24H0z",fill:"none"}))),null)},expandableRowsComponentProps:{},progressPending:!1,progressComponent:s.default.createElement("div",{style:{fontSize:"24px",fontWeight:700,padding:"24px"}},"Loading..."),persistTableHead:!1,sortIcon:null,sortFunction:null,sortServer:!1,striped:!1,highlightOnHover:!1,pointerOnHover:!1,noContextMenu:!1,contextMessage:{singular:"item",plural:"items",message:"selected"},actions:null,contextActions:null,contextComponent:null,defaultSortFieldId:null,defaultSortAsc:!0,responsive:!0,noDataComponent:s.default.createElement("div",{style:{padding:"24px"}},"There are no records to display"),disabled:!1,noTableHead:!1,noHeader:!1,subHeader:!1,subHeaderAlign:t.Alignment.RIGHT,subHeaderWrap:!0,subHeaderComponent:null,fixedHeader:!1,fixedHeaderScrollHeight:"100vh",pagination:!1,paginationServer:!1,paginationServerOptions:{persistSelectedOnSort:!1,persistSelectedOnPageChange:!1},paginationDefaultPage:1,paginationResetDefaultPage:!1,paginationTotalRows:0,paginationPerPage:10,paginationRowsPerPageOptions:[10,15,20,25,30],paginationComponent:null,paginationComponentOptions:{},paginationIconFirstPage:s.default.createElement((()=>s.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24","aria-hidden":"true",role:"presentation"},s.default.createElement("path",{d:"M18.41 16.59L13.82 12l4.59-4.59L17 6l-6 6 6 6zM6 6h2v12H6z"}),s.default.createElement("path",{fill:"none",d:"M24 24H0V0h24v24z"}))),null),paginationIconLastPage:s.default.createElement((()=>s.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24","aria-hidden":"true",role:"presentation"},s.default.createElement("path",{d:"M5.59 7.41L10.18 12l-4.59 4.59L7 18l6-6-6-6zM16 6h2v12h-2z"}),s.default.createElement("path",{fill:"none",d:"M0 0h24v24H0V0z"}))),null),paginationIconNext:s.default.createElement((()=>s.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24","aria-hidden":"true",role:"presentation"},s.default.createElement("path",{d:"M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"}),s.default.createElement("path",{d:"M0 0h24v24H0z",fill:"none"}))),null),paginationIconPrevious:s.default.createElement((()=>s.default.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24","aria-hidden":"true",role:"presentation"},s.default.createElement("path",{d:"M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"}),s.default.createElement("path",{d:"M0 0h24v24H0z",fill:"none"}))),null),dense:!1,conditionalRowStyles:[],theme:"default",customStyles:{},direction:t.Direction.AUTO,onChangePage:h,onChangeRowsPerPage:h,onRowClicked:h,onRowDoubleClicked:h,onRowMouseEnter:h,onRowMouseLeave:h,onRowExpandToggled:h,onSelectedRowsChange:h,onSort:h,onColumnOrderChange:h},He={rowsPerPageText:"Rows per page:",rangeSeparatorText:"of",noRowsPerPage:!1,selectAllRowsItem:!1,selectAllRowsItemText:"All"},je=d.default.nav`
	display: flex;
	flex: 1 1 auto;
	justify-content: flex-end;
	align-items: center;
	box-sizing: border-box;
	padding-right: 8px;
	padding-left: 8px;
	width: 100%;
	${({theme:e})=>e.pagination.style};
`,Fe=d.default.button`
	position: relative;
	display: block;
	user-select: none;
	border: none;
	${({theme:e})=>e.pagination.pageButtonsStyle};
	${({$isRTL:e})=>e&&"transform: scale(-1, -1)"};
`,Te=d.default.div`
	display: flex;
	align-items: center;
	border-radius: 4px;
	white-space: nowrap;
	${P`
    width: 100%;
    justify-content: space-around;
  `};
`,Ie=d.default.span`
	flex-shrink: 1;
	user-select: none;
`,Me=d.default(Ie)`
	margin: 0 24px;
`,Ae=d.default(Ie)`
	margin: 0 4px;
`;var Le=i.memo((function({rowsPerPage:e,rowCount:t,currentPage:n,direction:o=De.direction,paginationRowsPerPageOptions:a=De.paginationRowsPerPageOptions,paginationIconLastPage:l=De.paginationIconLastPage,paginationIconFirstPage:r=De.paginationIconFirstPage,paginationIconNext:s=De.paginationIconNext,paginationIconPrevious:d=De.paginationIconPrevious,paginationComponentOptions:c=De.paginationComponentOptions,onChangeRowsPerPage:g=De.onChangeRowsPerPage,onChangePage:u=De.onChangePage}){const p=(()=>{const e="object"==typeof window;function t(){return{width:e?window.innerWidth:void 0,height:e?window.innerHeight:void 0}}const[n,o]=i.useState(t);return i.useEffect((()=>{if(!e)return()=>null;function n(){o(t())}return window.addEventListener("resize",n),()=>window.removeEventListener("resize",n)}),[]),n})(),b=ie(o),m=p.width&&p.width>599,h=f(t,e),w=n*e,x=w-e+1,C=1===n,y=n===h,v=Object.assign(Object.assign({},He),c),R=n===h?`${x}-${t} ${v.rangeSeparatorText} ${t}`:`${x}-${w} ${v.rangeSeparatorText} ${t}`,S=i.useCallback((()=>u(n-1)),[n,u]),E=i.useCallback((()=>u(n+1)),[n,u]),O=i.useCallback((()=>u(1)),[u]),$=i.useCallback((()=>u(f(t,e))),[u,t,e]),P=i.useCallback((e=>g(Number(e.target.value),n)),[n,g]),k=a.map((e=>i.createElement("option",{key:e,value:e},e)));v.selectAllRowsItem&&k.push(i.createElement("option",{key:-1,value:t},v.selectAllRowsItemText));const D=i.createElement(ke,{onChange:P,defaultValue:e,"aria-label":v.rowsPerPageText},k);return i.createElement(je,{className:"rdt_Pagination"},!v.noRowsPerPage&&m&&i.createElement(i.Fragment,null,i.createElement(Ae,null,v.rowsPerPageText),D),m&&i.createElement(Me,null,R),i.createElement(Te,null,i.createElement(Fe,{id:"pagination-first-page",type:"button","aria-label":"First Page","aria-disabled":C,onClick:O,disabled:C,$isRTL:b},r),i.createElement(Fe,{id:"pagination-previous-page",type:"button","aria-label":"Previous Page","aria-disabled":C,onClick:S,disabled:C,$isRTL:b},d),!v.noRowsPerPage&&!m&&D,i.createElement(Fe,{id:"pagination-next-page",type:"button","aria-label":"Next Page","aria-disabled":y,onClick:E,disabled:y,$isRTL:b},s),i.createElement(Fe,{id:"pagination-last-page",type:"button","aria-label":"Last Page","aria-disabled":y,onClick:$,disabled:y,$isRTL:b},l)))}));const _e=(e,t)=>{const n=i.useRef(!0);i.useEffect((()=>{n.current?n.current=!1:e()}),t)};var ze=function(e){return function(e){return!!e&&"object"==typeof e}(e)&&!function(e){var t=Object.prototype.toString.call(e);return"[object RegExp]"===t||"[object Date]"===t||function(e){return e.$$typeof===Ne}(e)}(e)},Ne="function"==typeof Symbol&&Symbol.for?Symbol.for("react.element"):60103;function We(e,t){return!1!==t.clone&&t.isMergeableObject(e)?Ue((n=e,Array.isArray(n)?[]:{}),e,t):e;var n}function Be(e,t,n){return e.concat(t).map((function(e){return We(e,n)}))}function Ge(e){return Object.keys(e).concat(function(e){return Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(e).filter((function(t){return e.propertyIsEnumerable(t)})):[]}(e))}function Ve(e,t){try{return t in e}catch(e){return!1}}function Ue(e,t,n){(n=n||{}).arrayMerge=n.arrayMerge||Be,n.isMergeableObject=n.isMergeableObject||ze,n.cloneUnlessOtherwiseSpecified=We;var o=Array.isArray(t);return o===Array.isArray(e)?o?n.arrayMerge(e,t,n):function(e,t,n){var o={};return n.isMergeableObject(e)&&Ge(e).forEach((function(t){o[t]=We(e[t],n)})),Ge(t).forEach((function(a){(function(e,t){return Ve(e,t)&&!(Object.hasOwnProperty.call(e,t)&&Object.propertyIsEnumerable.call(e,t))})(e,a)||(Ve(e,a)&&n.isMergeableObject(t[a])?o[a]=function(e,t){if(!t.customMerge)return Ue;var n=t.customMerge(e);return"function"==typeof n?n:Ue}(a,n)(e[a],t[a],n):o[a]=We(t[a],n))})),o}(e,t,n):We(t,n)}Ue.all=function(e,t){if(!Array.isArray(e))throw new Error("first argument should be an array");return e.reduce((function(e,n){return Ue(e,n,t)}),{})};var Ye=Ue;const Ke={text:{primary:"rgba(0, 0, 0, 0.87)",secondary:"rgba(0, 0, 0, 0.54)",disabled:"rgba(0, 0, 0, 0.38)"},background:{default:"#FFFFFF"},context:{background:"#e3f2fd",text:"rgba(0, 0, 0, 0.87)"},divider:{default:"rgba(0,0,0,.12)"},button:{default:"rgba(0,0,0,.54)",focus:"rgba(0,0,0,.12)",hover:"rgba(0,0,0,.12)",disabled:"rgba(0, 0, 0, .18)"},selected:{default:"#e3f2fd",text:"rgba(0, 0, 0, 0.87)"},highlightOnHover:{default:"#EEEEEE",text:"rgba(0, 0, 0, 0.87)"},striped:{default:"#FAFAFA",text:"rgba(0, 0, 0, 0.87)"}},qe={default:Ke,light:Ke,dark:{text:{primary:"#FFFFFF",secondary:"rgba(255, 255, 255, 0.7)",disabled:"rgba(0,0,0,.12)"},background:{default:"#424242"},context:{background:"#E91E63",text:"#FFFFFF"},divider:{default:"rgba(81, 81, 81, 1)"},button:{default:"#FFFFFF",focus:"rgba(255, 255, 255, .54)",hover:"rgba(255, 255, 255, .12)",disabled:"rgba(255, 255, 255, .18)"},selected:{default:"rgba(0, 0, 0, .7)",text:"#FFFFFF"},highlightOnHover:{default:"rgba(0, 0, 0, .7)",text:"#FFFFFF"},striped:{default:"rgba(0, 0, 0, .87)",text:"#FFFFFF"}}};function Je(e,t,n,o){const[a,l]=i.useState((()=>b(e))),[s,d]=i.useState(""),c=i.useRef("");_e((()=>{l(b(e))}),[e]);const g=i.useCallback((e=>{var t,n,o;const{attributes:l}=e.target,r=null===(t=l.getNamedItem("data-column-id"))||void 0===t?void 0:t.value;r&&(c.current=(null===(o=null===(n=a[C(a,r)])||void 0===n?void 0:n.id)||void 0===o?void 0:o.toString())||"",d(c.current))}),[a]),u=i.useCallback((e=>{var n;const{attributes:o}=e.target,r=null===(n=o.getNamedItem("data-column-id"))||void 0===n?void 0:n.value;if(r&&c.current&&r!==c.current){const e=C(a,c.current),n=C(a,r),o=[...a];o[e]=a[n],o[n]=a[e],l(o),t(o)}}),[t,a]),p=i.useCallback((e=>{e.preventDefault()}),[]),f=i.useCallback((e=>{e.preventDefault()}),[]),m=i.useCallback((e=>{e.preventDefault(),c.current="",d("")}),[]),h=function(e=!1){return e?r.ASC:r.DESC}(o),w=i.useMemo((()=>a[C(a,null==n?void 0:n.toString())]||{}),[n,a]);return{tableColumns:a,draggingColumnId:s,handleDragStart:g,handleDragEnter:u,handleDragOver:p,handleDragLeave:f,handleDragEnd:m,defaultSortDirection:h,defaultSortColumn:w}}var Qe=i.memo((function(e){const{data:t=De.data,columns:n=De.columns,title:o=De.title,actions:l=De.actions,keyField:s=De.keyField,striped:d=De.striped,highlightOnHover:u=De.highlightOnHover,pointerOnHover:p=De.pointerOnHover,dense:b=De.dense,selectableRows:h=De.selectableRows,selectableRowsSingle:w=De.selectableRowsSingle,selectableRowsHighlight:C=De.selectableRowsHighlight,selectableRowsNoSelectAll:y=De.selectableRowsNoSelectAll,selectableRowsVisibleOnly:R=De.selectableRowsVisibleOnly,selectableRowSelected:E=De.selectableRowSelected,selectableRowDisabled:P=De.selectableRowDisabled,selectableRowsComponent:k=De.selectableRowsComponent,selectableRowsComponentProps:D=De.selectableRowsComponentProps,onRowExpandToggled:j=De.onRowExpandToggled,onSelectedRowsChange:F=De.onSelectedRowsChange,expandableIcon:T=De.expandableIcon,onChangeRowsPerPage:I=De.onChangeRowsPerPage,onChangePage:M=De.onChangePage,paginationServer:A=De.paginationServer,paginationServerOptions:L=De.paginationServerOptions,paginationTotalRows:_=De.paginationTotalRows,paginationDefaultPage:z=De.paginationDefaultPage,paginationResetDefaultPage:N=De.paginationResetDefaultPage,paginationPerPage:W=De.paginationPerPage,paginationRowsPerPageOptions:B=De.paginationRowsPerPageOptions,paginationIconLastPage:G=De.paginationIconLastPage,paginationIconFirstPage:V=De.paginationIconFirstPage,paginationIconNext:U=De.paginationIconNext,paginationIconPrevious:Y=De.paginationIconPrevious,paginationComponent:K=De.paginationComponent,paginationComponentOptions:q=De.paginationComponentOptions,responsive:J=De.responsive,progressPending:X=De.progressPending,progressComponent:Z=De.progressComponent,persistTableHead:ee=De.persistTableHead,noDataComponent:te=De.noDataComponent,disabled:ne=De.disabled,noTableHead:oe=De.noTableHead,noHeader:le=De.noHeader,fixedHeader:ie=De.fixedHeader,fixedHeaderScrollHeight:se=De.fixedHeaderScrollHeight,pagination:de=De.pagination,subHeader:ce=De.subHeader,subHeaderAlign:ge=De.subHeaderAlign,subHeaderWrap:ue=De.subHeaderWrap,subHeaderComponent:pe=De.subHeaderComponent,noContextMenu:be=De.noContextMenu,contextMessage:me=De.contextMessage,contextActions:he=De.contextActions,contextComponent:we=De.contextComponent,expandableRows:Oe=De.expandableRows,onRowClicked:$e=De.onRowClicked,onRowDoubleClicked:Pe=De.onRowDoubleClicked,onRowMouseEnter:ke=De.onRowMouseEnter,onRowMouseLeave:He=De.onRowMouseLeave,sortIcon:je=De.sortIcon,onSort:Fe=De.onSort,sortFunction:Te=De.sortFunction,sortServer:Ie=De.sortServer,expandableRowsComponent:Me=De.expandableRowsComponent,expandableRowsComponentProps:Ae=De.expandableRowsComponentProps,expandableRowDisabled:ze=De.expandableRowDisabled,expandableRowsHideExpander:Ne=De.expandableRowsHideExpander,expandOnRowClicked:We=De.expandOnRowClicked,expandOnRowDoubleClicked:Be=De.expandOnRowDoubleClicked,expandableRowExpanded:Ge=De.expandableRowExpanded,expandableInheritConditionalStyles:Ve=De.expandableInheritConditionalStyles,defaultSortFieldId:Ue=De.defaultSortFieldId,defaultSortAsc:Ke=De.defaultSortAsc,clearSelectedRows:Qe=De.clearSelectedRows,conditionalRowStyles:Xe=De.conditionalRowStyles,theme:Ze=De.theme,customStyles:et=De.customStyles,direction:tt=De.direction,onColumnOrderChange:nt=De.onColumnOrderChange,className:ot}=e,{tableColumns:at,draggingColumnId:lt,handleDragStart:rt,handleDragEnter:it,handleDragOver:st,handleDragLeave:dt,handleDragEnd:ct,defaultSortDirection:gt,defaultSortColumn:ut}=Je(n,nt,Ue,Ke),[{rowsPerPage:pt,currentPage:bt,selectedRows:ft,allSelected:mt,selectedCount:ht,selectedColumn:wt,sortDirection:xt,toggleOnSelectedRowsChange:Ct},yt]=i.useReducer(v,{allSelected:!1,selectedCount:0,selectedRows:[],selectedColumn:ut,toggleOnSelectedRowsChange:!1,sortDirection:gt,currentPage:z,rowsPerPage:W,selectedRowsFlag:!1,contextMessage:De.contextMessage}),{persistSelectedOnSort:vt=!1,persistSelectedOnPageChange:Rt=!1}=L,St=!(!A||!Rt&&!vt),Et=de&&!X&&t.length>0,Ot=K||Le,$t=i.useMemo((()=>((e={},t="default",n="default")=>{const o=qe[t]?t:n;return Ye({table:{style:{color:(a=qe[o]).text.primary,backgroundColor:a.background.default}},tableWrapper:{style:{display:"table"}},responsiveWrapper:{style:{}},header:{style:{fontSize:"22px",color:a.text.primary,backgroundColor:a.background.default,minHeight:"56px",paddingLeft:"16px",paddingRight:"8px"}},subHeader:{style:{backgroundColor:a.background.default,minHeight:"52px"}},head:{style:{color:a.text.primary,fontSize:"12px",fontWeight:500}},headRow:{style:{backgroundColor:a.background.default,minHeight:"52px",borderBottomWidth:"1px",borderBottomColor:a.divider.default,borderBottomStyle:"solid"},denseStyle:{minHeight:"32px"}},headCells:{style:{paddingLeft:"16px",paddingRight:"16px"},draggingStyle:{cursor:"move"}},contextMenu:{style:{backgroundColor:a.context.background,fontSize:"18px",fontWeight:400,color:a.context.text,paddingLeft:"16px",paddingRight:"8px",transform:"translate3d(0, -100%, 0)",transitionDuration:"125ms",transitionTimingFunction:"cubic-bezier(0, 0, 0.2, 1)",willChange:"transform"},activeStyle:{transform:"translate3d(0, 0, 0)"}},cells:{style:{paddingLeft:"16px",paddingRight:"16px",wordBreak:"break-word"},draggingStyle:{}},rows:{style:{fontSize:"13px",fontWeight:400,color:a.text.primary,backgroundColor:a.background.default,minHeight:"48px","&:not(:last-of-type)":{borderBottomStyle:"solid",borderBottomWidth:"1px",borderBottomColor:a.divider.default}},denseStyle:{minHeight:"32px"},selectedHighlightStyle:{"&:nth-of-type(n)":{color:a.selected.text,backgroundColor:a.selected.default,borderBottomColor:a.background.default}},highlightOnHoverStyle:{color:a.highlightOnHover.text,backgroundColor:a.highlightOnHover.default,transitionDuration:"0.15s",transitionProperty:"background-color",borderBottomColor:a.background.default,outlineStyle:"solid",outlineWidth:"1px",outlineColor:a.background.default},stripedStyle:{color:a.striped.text,backgroundColor:a.striped.default}},expanderRow:{style:{color:a.text.primary,backgroundColor:a.background.default}},expanderCell:{style:{flex:"0 0 48px"}},expanderButton:{style:{color:a.button.default,fill:a.button.default,backgroundColor:"transparent",borderRadius:"2px",transition:"0.25s",height:"100%",width:"100%","&:hover:enabled":{cursor:"pointer"},"&:disabled":{color:a.button.disabled},"&:hover:not(:disabled)":{cursor:"pointer",backgroundColor:a.button.hover},"&:focus":{outline:"none",backgroundColor:a.button.focus},svg:{margin:"auto"}}},pagination:{style:{color:a.text.secondary,fontSize:"13px",minHeight:"56px",backgroundColor:a.background.default,borderTopStyle:"solid",borderTopWidth:"1px",borderTopColor:a.divider.default},pageButtonsStyle:{borderRadius:"50%",height:"40px",width:"40px",padding:"8px",margin:"px",cursor:"pointer",transition:"0.4s",color:a.button.default,fill:a.button.default,backgroundColor:"transparent","&:disabled":{cursor:"unset",color:a.button.disabled,fill:a.button.disabled},"&:hover:not(:disabled)":{backgroundColor:a.button.hover},"&:focus":{outline:"none",backgroundColor:a.button.focus}}},noData:{style:{display:"flex",alignItems:"center",justifyContent:"center",color:a.text.primary,backgroundColor:a.background.default}},progress:{style:{display:"flex",alignItems:"center",justifyContent:"center",color:a.text.primary,backgroundColor:a.background.default}}},e);var a})(et,Ze)),[et,Ze]),Pt=i.useMemo((()=>Object.assign({},"auto"!==tt&&{dir:tt})),[tt]),kt=i.useMemo((()=>{if(Ie)return t;if((null==wt?void 0:wt.sortFunction)&&"function"==typeof wt.sortFunction){const e=wt.sortFunction,n=xt===r.ASC?e:(t,n)=>-1*e(t,n);return[...t].sort(n)}return function(e,t,n,o){return t?o&&"function"==typeof o?o(e.slice(0),t,n):e.slice(0).sort(((e,o)=>{let a,l;if("string"==typeof t?(a=g(e,t),l=g(o,t)):(a=t(e),l=t(o)),"asc"===n){if(a<l)return-1;if(a>l)return 1}if("desc"===n){if(a>l)return-1;if(a<l)return 1}return 0})):e}(t,null==wt?void 0:wt.selector,xt,Te)}),[Ie,wt,xt,t,Te]),Dt=i.useMemo((()=>{if(de&&!A){const e=bt*pt,t=e-pt;return kt.slice(t,e)}return kt}),[bt,de,A,pt,kt]),Ht=i.useCallback((e=>{yt(e)}),[]),jt=i.useCallback((e=>{yt(e)}),[]),Ft=i.useCallback((e=>{yt(e)}),[]),Tt=i.useCallback(((e,t)=>$e(e,t)),[$e]),It=i.useCallback(((e,t)=>Pe(e,t)),[Pe]),Mt=i.useCallback(((e,t)=>ke(e,t)),[ke]),At=i.useCallback(((e,t)=>He(e,t)),[He]),Lt=i.useCallback((e=>yt({type:"CHANGE_PAGE",page:e,paginationServer:A,visibleOnly:R,persistSelectedOnPageChange:Rt})),[A,Rt,R]),_t=i.useCallback((e=>{const t=f(_||Dt.length,e),n=m(bt,t);A||Lt(n),yt({type:"CHANGE_ROWS_PER_PAGE",page:n,rowsPerPage:e})}),[bt,Lt,A,_,Dt.length]);if(de&&!A&&kt.length>0&&0===Dt.length){const e=f(kt.length,pt),t=m(bt,e);Lt(t)}_e((()=>{F({allSelected:mt,selectedCount:ht,selectedRows:ft.slice(0)})}),[Ct]),_e((()=>{Fe(wt,xt,kt.slice(0))}),[wt,xt]),_e((()=>{M(bt,_||kt.length)}),[bt]),_e((()=>{I(pt,bt)}),[pt]),_e((()=>{Lt(z)}),[z,N]),_e((()=>{if(de&&A&&_>0){const e=f(_,pt),t=m(bt,e);bt!==t&&Lt(t)}}),[_]),i.useEffect((()=>{yt({type:"CLEAR_SELECTED_ROWS",selectedRowsFlag:Qe})}),[w,Qe]),i.useEffect((()=>{if(!E)return;const e=kt.filter((e=>E(e))),t=w?e.slice(0,1):e;yt({type:"SELECT_MULTIPLE_ROWS",keyField:s,selectedRows:t,totalRows:kt.length,mergeSelections:St})}),[t,E]);const zt=R?Dt:kt,Nt=Rt||w||y;return i.createElement(a.ThemeProvider,{theme:$t},!le&&(!!o||!!l)&&i.createElement(fe,{title:o,actions:l,showMenu:!be,selectedCount:ht,direction:tt,contextActions:he,contextComponent:we,contextMessage:me}),ce&&i.createElement(xe,{align:ge,wrapContent:ue},pe),i.createElement(ye,Object.assign({$responsive:J,$fixedHeader:ie,$fixedHeaderScrollHeight:se,className:ot},Pt),i.createElement(Re,null,X&&!ee&&i.createElement(ve,null,Z),i.createElement(S,{disabled:ne,className:"rdt_Table",role:"table"},!oe&&(!!ee||kt.length>0&&!X)&&i.createElement(O,{className:"rdt_TableHead",role:"rowgroup",$fixedHeader:ie},i.createElement($,{className:"rdt_TableHeadRow",role:"row",$dense:b},h&&(Nt?i.createElement(H,{style:{flex:"0 0 48px"}}):i.createElement(re,{allSelected:mt,selectedRows:ft,selectableRowsComponent:k,selectableRowsComponentProps:D,selectableRowDisabled:P,rowData:zt,keyField:s,mergeSelections:St,onSelectAllRows:jt})),Oe&&!Ne&&i.createElement(Se,null),at.map((e=>i.createElement(ae,{key:e.id,column:e,selectedColumn:wt,disabled:X||0===kt.length,pagination:de,paginationServer:A,persistSelectedOnSort:vt,selectableRowsVisibleOnly:R,sortDirection:xt,sortIcon:je,sortServer:Ie,onSort:Ht,onDragStart:rt,onDragOver:st,onDragEnd:ct,onDragEnter:it,onDragLeave:dt,draggingColumnId:lt}))))),!kt.length&&!X&&i.createElement(Ee,null,te),X&&ee&&i.createElement(ve,null,Z),!X&&kt.length>0&&i.createElement(Ce,{className:"rdt_TableBody",role:"rowgroup"},Dt.map(((e,t)=>{const n=c(e,s),o=function(e=""){return"number"!=typeof e&&(!e||0===e.length)}(n)?t:n,a=x(e,ft,s),l=!!(Oe&&Ge&&Ge(e)),r=!!(Oe&&ze&&ze(e));return i.createElement(Q,{id:o,key:o,keyField:s,"data-row-id":o,columns:at,row:e,rowCount:kt.length,rowIndex:t,selectableRows:h,expandableRows:Oe,expandableIcon:T,highlightOnHover:u,pointerOnHover:p,dense:b,expandOnRowClicked:We,expandOnRowDoubleClicked:Be,expandableRowsComponent:Me,expandableRowsComponentProps:Ae,expandableRowsHideExpander:Ne,defaultExpanderDisabled:r,defaultExpanded:l,expandableInheritConditionalStyles:Ve,conditionalRowStyles:Xe,selected:a,selectableRowsHighlight:C,selectableRowsComponent:k,selectableRowsComponentProps:D,selectableRowDisabled:P,selectableRowsSingle:w,striped:d,onRowExpandToggled:j,onRowClicked:Tt,onRowDoubleClicked:It,onRowMouseEnter:Mt,onRowMouseLeave:At,onSelectedRow:Ft,draggingColumnId:lt,onDragStart:rt,onDragOver:st,onDragEnd:ct,onDragEnter:it,onDragLeave:dt})})))))),Et&&i.createElement("div",null,i.createElement(Ot,{onChangePage:Lt,onChangeRowsPerPage:_t,rowCount:_||kt.length,currentPage:bt,rowsPerPage:pt,direction:tt,paginationRowsPerPageOptions:B,paginationIconLastPage:G,paginationIconFirstPage:V,paginationIconNext:U,paginationIconPrevious:Y,paginationComponentOptions:q})))}));t.STOP_PROP_TAG="allowRowEvents",t.createTheme=function(e="default",t,n="default"){return qe[e]||(qe[e]=Ye(qe[n],t||{})),qe[e]=Ye(qe[e],t||{}),qe[e]},t.default=Qe,t.defaultThemes=qe}}]);