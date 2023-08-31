import { Executor } from './exec';

export async function computeDataFrame(dfName: string, dfString: string) {
  if (!dfName) {
    return Promise.resolve();
  }

  return await Executor.execute(
    Executor.withJson(
      Executor.withPandas(
        Executor.withIDE(
          `dfName="${dfName}"\nIDE.DataFrameStorage.add(dfName, pd.read_json('${dfString}'))\ndfName`
        )
      )
    )
  );
}
