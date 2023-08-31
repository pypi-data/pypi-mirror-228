import { IRenderMime, RenderedCommon } from '@jupyterlab/rendermime';
import { Panel, PanelLayout } from '@lumino/widgets';
import { RenderedDataTable } from '../../sidebar/datatable';
import { RenderedSidebar } from '../../sidebar/renderer';
import { IDEGlobal, Nullable } from '../../utils';
import { TrrackableCell, TrrackableCellId } from '../trrackableCell';
import { OutputHeaderWidget } from './OutputHeader';
import { OutputLoaderWidget } from './OutputLoader';

export const EXECUTE_RESULT_CLASS = 'jp-persist-OutputArea-executeResult';
export const OUTPUT_AREA_ORIGINAL_CLASS = 'jp-OutputArea-output'; // The original class from JupyterLab
export const GRID_AREA_OUTPUT = 'jp-gridArea-OutputArea-output';
export const ENABLE_SCROLL = 'enable-scroll';

const OUTPUT_AREA_CLASS = 'jp-persist-OutputArea-output';
const SIDEBAR_VIS_CLASS = 'jp-persist-OutputArea-sidebar';
const GRID_AREA_HEAD = 'jp-gridArea-OutputArea-head';
const GRID_AREA_SIDEBAR = 'jp-gridArea-OutputArea-sidebar';

const SIDEBAR_SECTION_ID = 'sidebar';

const REGULAR_SECTION_ID = 'regular';

const OUTPUT_AREA_CONTAINER = 'jp-persist-output-container';
const OUTPUT_LOADER_OVERLAY = 'jp-persist-loader-overlay';

export abstract class RenderedSidebarOutput extends RenderedCommon {
  private _createRenderer: () => IRenderMime.IRenderer; // Wrapper for createRenderer with opts passed.
  private _sidebarRenderer: RenderedSidebar; // Trrack vis renderer
  private _datatableRenderer: RenderedDataTable; // Trrack vis renderer

  private _executeResultRenderer: IRenderMime.IRenderer | RenderedDataTable; // latest renderer created by _createRenderer

  protected outputHeaderWidget = new OutputHeaderWidget(); // Output header widget
  protected outputArea = new Panel(); // Output area widget
  protected sidebarWidget = new Panel(); // TrrackVis Widget

  protected _panelLayout: PanelLayout; // New layout for RenderedCommon instance

  constructor(_options: IRenderMime.IRendererOptions) {
    super(_options);

    // Replace default layout
    this.layout = this._panelLayout = new PanelLayout();
    this.addClass('lm-Panel');

    this.addClass(OUTPUT_AREA_CLASS); // Add new output area class

    // Setup outputArea widget
    this._setupOutputHeaderWidget(); // Setup output header widget

    // Setup execute result renderer & widget
    this._createRenderer = () => this.createRenderer(_options); // set the wrapper
    this._executeResultRenderer = this._createRenderer(); // create the first renderer
    this._setupExecuteResultWidget(); // Setup output area widget

    // Setup trrack render & widget
    this._sidebarRenderer = new RenderedSidebar(); // Create trrack vis renderer
    this._datatableRenderer = new RenderedDataTable(); // Create data table renderer

    this._setupSidebarWidget(); // Setup trrack vis widget

    // Add all widgets to output layout
    this._panelLayout.addWidget(this.outputHeaderWidget);
    this._panelLayout.addWidget(this.outputArea);
    this._panelLayout.addWidget(this.sidebarWidget);
  }

  protected abstract postRender(cell: TrrackableCell): Promise<void>;

  protected abstract createRenderer(
    opts: IRenderMime.IRendererOptions
  ): IRenderMime.IRenderer;

  get executeResultRenderer() {
    return this._executeResultRenderer;
  }

  _setupOutputHeaderWidget() {
    this.outputHeaderWidget.addClass(GRID_AREA_HEAD); // add grid-area name
  }

  _setupExecuteResultWidget() {
    this.outputArea.id = REGULAR_SECTION_ID; // Add output area id
    this.outputArea.addClass(GRID_AREA_OUTPUT);
    this.outputArea.addClass(EXECUTE_RESULT_CLASS);
    this.outputArea.addClass(OUTPUT_AREA_ORIGINAL_CLASS); // add the original output class from jupyterlab
    this.outputArea.addClass(ENABLE_SCROLL); // enable overflow scroll
  }

  _setupSidebarWidget() {
    this.sidebarWidget.id = SIDEBAR_SECTION_ID; // add trrack id
    this.sidebarWidget.addClass(GRID_AREA_SIDEBAR);
    this.sidebarWidget.addClass(SIDEBAR_VIS_CLASS);
    this.sidebarWidget.addWidget(this._sidebarRenderer);
  }

  /**
   * This is the default class
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    this.toggleClass('jp-mod-trusted', model.trusted); // add trusted class

    // Render the content.
    await this.render(model);

    // Handle the fragment identifier if given. Not sure what this does, but it
    // is done in most implementations of RenderedCommon
    const { fragment } = model.metadata || {};
    if (fragment) {
      this.setFragment(fragment as string);
    }
  }

  /**
   * New render logic for output area
   * Makes sure the updates happen without flickering the screen.
   * Should explore if this is the best way to do this. Maybe inefficient for larger outputs.
   */
  async render(model: IRenderMime.IMimeModel): Promise<void> {
    // Get the id of the cell from metadata
    // Create new renderer instance
    const renderer = this._createRenderer();

    if (!model.metadata.dataframeOnly) {
      await renderer.renderModel(model);
    }

    if (!this.outputArea.layout) {
      return;
    }

    // why this check? explorfe
    // Remove old outputs
    while (this.outputArea.widgets.length > 0) {
      (this.outputArea.layout as PanelLayout).widgets[0].dispose();
      (this.outputArea.layout as PanelLayout).removeWidgetAt(0);
    }

    // Make sure the HTML is empty
    this.outputArea.node.textContent = '';

    // Add new renderer widget
    const outputAreaPanel = new Panel();
    outputAreaPanel.addClass(OUTPUT_AREA_CONTAINER);

    const outputLoadingOverlay = new OutputLoaderWidget();
    outputLoadingOverlay.addClass(OUTPUT_LOADER_OVERLAY);
    outputLoadingOverlay.show();

    outputAreaPanel.addWidget(renderer);
    outputAreaPanel.addWidget(outputLoadingOverlay);
    this.outputArea.addWidget(
      model.metadata.dataframeOnly ? this._datatableRenderer : outputAreaPanel
    );

    // Dispose old renderer
    this._executeResultRenderer.dispose();

    // Set new renderer to public API
    this._executeResultRenderer = model.metadata.dataframeOnly
      ? this._datatableRenderer
      : renderer;

    // Get cellId for output are

    const id = model.metadata?.cellId as Nullable<TrrackableCellId>;

    const cell = id ? IDEGlobal.cells.get(id) : null;

    if (!id) {
      console.warn(
        'Cell id not found in metadata for following element. Consider not using RenderedTrrackOutput'
      );
      console.warn(this.node);
    }

    // Get cell from id

    // If cell is not found, or trrackVisRenderer is not found, hide the output area
    if (!id || !cell || !this._sidebarRenderer) {
      this.outputHeaderWidget.hide();
      this._sidebarRenderer?.hide();
      this._datatableRenderer.hide();
    } else {
      // Associate the cell with the output header widget
      this.outputHeaderWidget.associateCell(cell);

      outputLoadingOverlay.associateCell(cell);

      // Render the trrack vis
      this._sidebarRenderer.tryRender(cell);

      // Post render logic if set

      if (model.metadata.dataframeOnly) {
        this._datatableRenderer.tryRender(
          cell,
          JSON.parse(model.data['application/vnd.vega.v5+json'] as any)
        );
      }

      this.postRender(cell);
    }

    return;
  }

  dispose() {
    super.dispose();

    this._executeResultRenderer.dispose();
    this._sidebarRenderer.dispose();
    this.outputHeaderWidget.dispose();
  }
}
