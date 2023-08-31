import { State, hookstate } from '@hookstate/core';
import { ISignal, Signal } from '@lumino/signaling';
import { NodeId, Trigger } from '@trrack/core';
import { compressToUTF16, decompressFromUTF16 } from 'lz-string';
import { TrrackableCell } from '../cells/trrackableCell';
import { Disposable, Nullable } from '../utils';
import { Trrack, TrrackOps } from './init';
import { TrrackActions, TrrackNode } from './types';

const TRRACK_GRAPH_KEY = 'trrack_graph';

export type TrrackCurrentChange = {
  currentNode: TrrackNode;
  trigger: Trigger | 'reset';
  state: ReturnType<Trrack['getState']>;
};

// TODO: refactor with hookstate

export class TrrackManager extends Disposable {
  private _trrack: Trrack;
  private _actions: TrrackActions;
  private _trrackInstanceChange = new Signal<this, string>(this);
  private _trrackCurrentChange = new Signal<this, TrrackCurrentChange>(this);

  currentState: State<NodeId>;

  constructor(public _cell: TrrackableCell) {
    super();
    const { trrack, actions } = this._reset(true);

    this._trrack = trrack;
    this._actions = actions;
    this.currentState = hookstate(trrack.current.id);

    this.trrack.currentChange(() => this.currentState.set(trrack.current.id));
  }

  get savedGraph(): Nullable<string> {
    const graph = this._cell.model.getMetadata(TRRACK_GRAPH_KEY) as
      | string
      | undefined;

    // return null for no graph
    if (!graph) {
      return null;
    }

    // Stringify and load graph
    if (typeof graph !== 'string') {
      return JSON.stringify(graph);
    }

    // return uncompressed graph
    if (
      graph.includes('current') &&
      graph.includes('root') &&
      graph.includes('nodes')
    ) {
      return graph;
    }

    // decompress and return uncompressed graph
    return decompressFromUTF16(graph);
  }

  get hasSelections() {
    const interaction = this._cell.trrackManager.trrack.getState();

    if (interaction.type === 'selection') {
      const { selected } = interaction;

      return !!selected;
    }

    if (interaction.type === 'intent') {
      return true;
    }

    if (interaction.type === 'invert-selection') {
      return true;
    }

    return false;
  }

  get trrack() {
    return this._trrack;
  }

  get actions() {
    return this._actions;
  }

  get isAtRoot() {
    return this.current === this.root;
  }

  get isAtLatest() {
    return this._trrack.current.children.length === 0;
  }

  get hasOnlyRoot() {
    return this._trrack.root.children.length === 0;
  }

  get changed(): ISignal<this, string> {
    return this._trrackInstanceChange;
  }

  get currentChange(): ISignal<this, TrrackCurrentChange> {
    return this._trrackCurrentChange;
  }

  get root() {
    return this._trrack.root.id;
  }

  get current() {
    return this._trrack.current.id;
  }

  private _reset(loadGraph: boolean) {
    this.currentChange.disconnect(this._saveTrrackGraphToModel, this);

    const { trrack, actions } = TrrackOps.create(
      loadGraph ? this.savedGraph : undefined
    );
    this._trrack = trrack;
    this._actions = actions;

    this._saveTrrackGraphToModel();

    this._trrack.currentChange((trigger?: Trigger) => {
      this._trrackCurrentChange.emit({
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        trigger: trigger!,
        currentNode: this._trrack.current,
        state: this._trrack.getState()
      });
    });

    this.currentChange.connect(this._saveTrrackGraphToModel, this);

    this._trrackInstanceChange.emit(this._trrack.root.id);
    this._trrackCurrentChange.emit({
      trigger: 'reset',
      currentNode: this._trrack.current,
      state: this._trrack.getState()
    });

    return { trrack, actions };
  }

  private _saveTrrackGraphToModel() {
    this._cell.model.setMetadata(
      TRRACK_GRAPH_KEY,
      compressToUTF16(this._trrack.export())
    );
  }

  reset() {
    this._reset(false);
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this.isDisposed = true;
    Signal.clearData(this);
  }
}
