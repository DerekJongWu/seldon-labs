"use client";
import { useState } from "react";

type Variable = {
  variable: string;
  variableNumber: string;
  desiredEffect: string;
  dataType: string;
  mean: string;
  max: string;
  min: string;
  weight: string;
};

export default function Home() {
  const [variables, setVariables] = useState<Variable[]>([
    {
      variable: "",
      variableNumber: "",
      desiredEffect: "Positive",
      dataType: "",
      mean: "",
      max: "",
      min: "",
      weight: "",
    },
  ]);

  const [variablesB, setVariablesB] = useState<Variable[]>([
    {
      variable: "",
      variableNumber: "",
      desiredEffect: "Positive",
      dataType: "",
      mean: "",
      max: "",
      min: "",
      weight: "",
    },
  ]);

  const handleChange = (index: number, field: keyof Variable, value: string) => {
    const newVariables = [...variables];
    newVariables[index][field] = value;
    setVariables(newVariables);
  };

  const handleChangeB = (index: number, field: keyof Variable, value: string) => {
    const newVariables = [...variablesB];
    newVariables[index][field] = value;
    setVariablesB(newVariables);
  };

  const addVariable = () => {
    setVariables([
      ...variables,
      {
        variable: "",
        variableNumber: "",
        desiredEffect: "Positive",
        dataType: "",
        mean: "",
        max: "",
        min: "",
        weight: "",
      },
    ]);
  };

  const addVariableB = () => {
    setVariablesB([
      ...variablesB,
      {
        variable: "",
        variableNumber: "",
        desiredEffect: "Positive",
        dataType: "",
        mean: "",
        max: "",
        min: "",
        weight: "",
      },
    ]);
  };

  const removeVariable = (index: number) => {
    setVariables(variables.filter((_, i) => i !== index));
  };

  const removeVariableB = (index: number) => {
    setVariablesB(variablesB.filter((_, i) => i !== index));
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[48px] row-start-2 items-center sm:items-start w-full max-w-4xl">
        {/* Player A Section */}
        <section className="w-full">
          <h2 className="text-lg font-bold text-red-600 mb-2">PLAYER A INFORMATION</h2>
          <h3 className="text-base font-semibold mb-4">Player A Historical Data</h3>
          <div className="overflow-x-auto w-full">
            <table className="min-w-full border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold">Variable</th>
                  <th className="p-2 font-semibold">Variable Number</th>
                  <th className="p-2 font-semibold">Desired Effect</th>
                  <th className="p-2 font-semibold">Data Type</th>
                  <th className="p-2 font-semibold">Mean</th>
                  <th className="p-2 font-semibold">Max</th>
                  <th className="p-2 font-semibold">Min</th>
                  <th className="p-2 font-semibold">Weight</th>
                  <th className="p-2 font-semibold">Remove</th>
                </tr>
              </thead>
              <tbody>
                {variables.map((v, idx) => (
                  <tr key={idx} className="even:bg-gray-50 dark:even:bg-gray-900">
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-28 sm:w-32 px-1 py-0.5 border rounded"
                        value={v.variable}
                        onChange={e => handleChange(idx, "variable", e.target.value)}
                        placeholder="e.g. GDP Growth"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.variableNumber}
                        onChange={e => handleChange(idx, "variableNumber", e.target.value)}
                        placeholder="e.g. v1"
                      />
                    </td>
                    <td className="p-2">
                      <select
                        className="w-20 px-1 py-0.5 border rounded"
                        value={v.desiredEffect}
                        onChange={e => handleChange(idx, "desiredEffect", e.target.value)}
                      >
                        <option value="Positive">Positive</option>
                        <option value="Negative">Negative</option>
                      </select>
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-20 px-1 py-0.5 border rounded"
                        value={v.dataType}
                        onChange={e => handleChange(idx, "dataType", e.target.value)}
                        placeholder="e.g. Econ"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.mean}
                        onChange={e => handleChange(idx, "mean", e.target.value)}
                        placeholder="e.g. 2.9%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.max}
                        onChange={e => handleChange(idx, "max", e.target.value)}
                        placeholder="e.g. 8%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.min}
                        onChange={e => handleChange(idx, "min", e.target.value)}
                        placeholder="e.g. -3%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-14 px-1 py-0.5 border rounded"
                        value={v.weight}
                        onChange={e => handleChange(idx, "weight", e.target.value)}
                        placeholder="e.g. 0.20"
                      />
                    </td>
                    <td className="p-2 text-center">
                      {variables.length > 1 && (
                        <button
                          type="button"
                          className="text-red-500 hover:text-red-700 font-bold px-2"
                          onClick={() => removeVariable(idx)}
                          aria-label="Remove variable"
                        >
                          ×
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button
              type="button"
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              onClick={addVariable}
            >
              + Add Variable
            </button>
          </div>
        </section>
        {/* Player B Section */}
        <section className="w-full">
          <h2 className="text-lg font-bold text-blue-600 mb-2">PLAYER B INFORMATION</h2>
          <h3 className="text-base font-semibold mb-4">Player B Historical Data</h3>
          <div className="overflow-x-auto w-full">
            <table className="min-w-full border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold">Variable</th>
                  <th className="p-2 font-semibold">Variable Number</th>
                  <th className="p-2 font-semibold">Desired Effect</th>
                  <th className="p-2 font-semibold">Data Type</th>
                  <th className="p-2 font-semibold">Mean</th>
                  <th className="p-2 font-semibold">Max</th>
                  <th className="p-2 font-semibold">Min</th>
                  <th className="p-2 font-semibold">Weight</th>
                  <th className="p-2 font-semibold">Remove</th>
                </tr>
              </thead>
              <tbody>
                {variablesB.map((v, idx) => (
                  <tr key={idx} className="even:bg-gray-50 dark:even:bg-gray-900">
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-28 sm:w-32 px-1 py-0.5 border rounded"
                        value={v.variable}
                        onChange={e => handleChangeB(idx, "variable", e.target.value)}
                        placeholder="e.g. GDP Growth"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.variableNumber}
                        onChange={e => handleChangeB(idx, "variableNumber", e.target.value)}
                        placeholder="e.g. v1"
                      />
                    </td>
                    <td className="p-2">
                      <select
                        className="w-20 px-1 py-0.5 border rounded"
                        value={v.desiredEffect}
                        onChange={e => handleChangeB(idx, "desiredEffect", e.target.value)}
                      >
                        <option value="Positive">Positive</option>
                        <option value="Negative">Negative</option>
                      </select>
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-20 px-1 py-0.5 border rounded"
                        value={v.dataType}
                        onChange={e => handleChangeB(idx, "dataType", e.target.value)}
                        placeholder="e.g. Econ"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.mean}
                        onChange={e => handleChangeB(idx, "mean", e.target.value)}
                        placeholder="e.g. 2.9%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.max}
                        onChange={e => handleChangeB(idx, "max", e.target.value)}
                        placeholder="e.g. 8%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-16 px-1 py-0.5 border rounded"
                        value={v.min}
                        onChange={e => handleChangeB(idx, "min", e.target.value)}
                        placeholder="e.g. -3%"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="text"
                        className="w-14 px-1 py-0.5 border rounded"
                        value={v.weight}
                        onChange={e => handleChangeB(idx, "weight", e.target.value)}
                        placeholder="e.g. 0.20"
                      />
                    </td>
                    <td className="p-2 text-center">
                      {variablesB.length > 1 && (
                        <button
                          type="button"
                          className="text-red-500 hover:text-red-700 font-bold px-2"
                          onClick={() => removeVariableB(idx)}
                          aria-label="Remove variable"
                        >
                          ×
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button
              type="button"
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              onClick={addVariableB}
            >
              + Add Variable
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
