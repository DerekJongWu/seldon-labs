"use client";
import { useState } from "react";
import React from "react";

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

  const scenarios = ["NT_NT", "T_NT", "NT_T", "T_T"];

  // For Player A
  const [scenarioValuesA, setScenarioValuesA] = useState(
    scenarios.map(() => variables.map(() => ""))
  );

  const handleScenarioChangeA = (scenarioIdx: number, varIdx: number, value: string) => {
    const updated = scenarioValuesA.map((row, i) =>
      i === scenarioIdx ? row.map((v, j) => (j === varIdx ? value : v)) : row
    );
    setScenarioValuesA(updated);
  };

  // For Player B
  const [scenarioValuesB, setScenarioValuesB] = useState(
    scenarios.map(() => variablesB.map(() => ""))
  );

  const handleScenarioChangeB = (scenarioIdx: number, varIdx: number, value: string) => {
    const updated = scenarioValuesB.map((row, i) =>
      i === scenarioIdx ? row.map((v, j) => (j === varIdx ? value : v)) : row
    );
    setScenarioValuesB(updated);
  };

  // Helper to get numeric value from string (handles %)
  const parseNumber = (val: string) => {
    if (!val) return NaN;
    if (val.includes("%")) return parseFloat(val.replace("%", ""));
    return parseFloat(val);
  };

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
    setVariables(prev => {
      const newVars = [
        ...prev,
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
      ];
      setScenarioValuesA(prevScenarioValues =>
        prevScenarioValues.map(row => [...row, ""])
      );
      return newVars;
    });
  };

  const addVariableB = () => {
    setVariablesB(prev => {
      const newVars = [
        ...prev,
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
      ];
      setScenarioValuesB(prevScenarioValues =>
        prevScenarioValues.map(row => [...row, ""])
      );
      return newVars;
    });
  };

  const removeVariable = (index: number) => {
    setVariables(prev => {
      const newVars = prev.filter((_, i) => i !== index);
      setScenarioValuesA(prevScenarioValues =>
        prevScenarioValues.map(row => row.filter((_, i) => i !== index))
      );
      return newVars;
    });
  };

  const removeVariableB = (index: number) => {
    setVariablesB(prev => {
      const newVars = prev.filter((_, i) => i !== index);
      setScenarioValuesB(prevScenarioValues =>
        prevScenarioValues.map(row => row.filter((_, i) => i !== index))
      );
      return newVars;
    });
  };

  // Add state for formula input for Player A and Player B
  const [formulaA, setFormulaA] = useState("");
  const [formulaB, setFormulaB] = useState("");

  // Helper to safely evaluate formula
  function safeEval(formula: string, vars: Record<string, number>) {
    try {
      // Allow variable names with letters, numbers, and underscores
      const allowed = /^[\d\s+\-*/().a-zA-Z0-9_]+$/;
      if (!allowed.test(formula)) return "";
      let expr = formula;
      Object.entries(vars).forEach(([k, v]) => {
        expr = expr.replaceAll(k, v.toString());
      });
      // eslint-disable-next-line no-eval
      return eval(expr);
    } catch {
      return "";
    }
  }

  // Add state for API response and loading
  const [apiResponse, setApiResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Helper to gather all data for submission
  const gatherSubmissionData = () => {
    // Prepare variables for both players
    const playerA = {
      variables,
      scenarioValues: scenarioValuesA,
      formula: formulaA,
      scenarios,
    };
    const playerB = {
      variables: variablesB,
      scenarioValues: scenarioValuesB,
      formula: formulaB,
      scenarios,
    };
    // Optionally, you can also send payoff results if you want
    return { playerA, playerB };
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setApiResponse(null);
    try {
      const data = gatherSubmissionData();
      const res = await fetch("/api/:path*", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const result = await res.json();
      setApiResponse(JSON.stringify(result, null, 2));
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
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
          <div className="mt-8">
            <h4 className="font-semibold mb-2">Scenarios</h4>
            <table className="min-w-full border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold border">Scenario</th>
                  {variables.map((v, idx) => (
                    <th key={idx} colSpan={2} className="p-2 font-semibold border text-center">
                      {v.variableNumber}: {v.variable}
                    </th>
                  ))}
                </tr>
                <tr>
                  <th></th>
                  {variables.map((_, idx) => (
                    <React.Fragment key={idx}>
                      <th className="p-2 font-semibold border">Value</th>
                      <th className="p-2 font-semibold border">Std</th>
                    </React.Fragment>
                  ))}
                </tr>
              </thead>
              <tbody>
                {scenarios.map((scenario, sIdx) => (
                  <tr key={scenario}>
                    <td className="p-2 font-semibold border">{scenario}</td>
                    {variables.map((v, vIdx) => {
                      const scenarioVal = scenarioValuesA[sIdx]?.[vIdx] || "";
                      const inputVal = parseNumber(scenarioVal);
                      const minVal = parseNumber(v.min);
                      const maxVal = parseNumber(v.max);
                      const stdNum = isNaN(inputVal) || isNaN(minVal) || isNaN(maxVal) || maxVal === minVal
                        ? 0
                        : (inputVal - minVal) / (maxVal - minVal);
                      const std = isNaN(inputVal) || isNaN(minVal) || isNaN(maxVal) || maxVal === minVal
                        ? ""
                        : stdNum.toFixed(2);
                      return (
                        <React.Fragment key={vIdx}>
                          <td className="p-2 border text-center">
                            <input
                              type="text"
                              className="w-16 px-1 py-0.5 border rounded"
                              value={scenarioVal}
                              onChange={e => handleScenarioChangeA(sIdx, vIdx, e.target.value)}
                              placeholder="Value"
                            />
                          </td>
                          <td className="p-2 border text-center">
                            {std}
                          </td>
                        </React.Fragment>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-8">
            <h4 className="font-semibold mb-2">Payoff Formula</h4>
            <div className="flex items-center gap-2 mb-2">
              <label htmlFor="formulaA" className="font-mono text-xs">Formula:</label>
              <input
                id="formulaA"
                type="text"
                className="w-full max-w-md px-2 py-1 border rounded font-mono text-xs"
                value={formulaA}
                onChange={e => setFormulaA(e.target.value)}
                placeholder="e.g. (v1_Stnd*0.2)+(v2_Stnd*0.2)+(v3_Stnd*0.4)+(v4_Stnd*0.1)+(v5_Stnd*0.1)"
              />
            </div>
            <table className="min-w-[300px] border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold border">Scenario</th>
                  <th className="p-2 font-semibold border">Payoff Formula Result</th>
                </tr>
              </thead>
              <tbody>
                {scenarios.map((scenario, sIdx) => {
                  // Build variable map: v1_Stnd, v2_Stnd, ... and v1_Val, v2_Val, ...
                  const vars: Record<string, number> = {};
                  variables.forEach((v, vIdx) => {
                    const inputVal = parseNumber(scenarioValuesA[sIdx]?.[vIdx] || "");
                    const stdNum = isNaN(inputVal) || isNaN(parseNumber(v.min)) || isNaN(parseNumber(v.max)) || parseNumber(v.max) === parseNumber(v.min)
                      ? 0
                      : (inputVal - parseNumber(v.min)) / (parseNumber(v.max) - parseNumber(v.min));
                    vars[`v${vIdx + 1}_Stnd`] = stdNum;
                    vars[`v${vIdx + 1}_Val`] = isNaN(inputVal) ? 0 : inputVal;
                    vars[`v${vIdx + 1}_mean`] = isNaN(parseNumber(v.mean)) ? 0 : parseNumber(v.mean);
                    vars[`v${vIdx + 1}_max`] = isNaN(parseNumber(v.max)) ? 0 : parseNumber(v.max);
                    vars[`v${vIdx + 1}_min`] = isNaN(parseNumber(v.min)) ? 0 : parseNumber(v.min);
                    vars[`v${vIdx + 1}_weight`] = isNaN(parseNumber(v.weight)) ? 0 : parseNumber(v.weight);
                  });
                  const result = formulaA ? safeEval(formulaA, vars) : "";
                  return (
                    <tr key={scenario}>
                      <td className="p-2 border font-semibold">{scenario}</td>
                      <td className="p-2 border text-right">{result !== "" ? Number(result).toFixed(4) : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
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
          <div className="mt-8">
            <h4 className="font-semibold mb-2">Scenarios</h4>
            <table className="min-w-full border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold border">Scenario</th>
                  {variablesB.map((v, idx) => (
                    <th key={idx} colSpan={2} className="p-2 font-semibold border text-center">
                      {v.variableNumber}: {v.variable}
                    </th>
                  ))}
                </tr>
                <tr>
                  <th></th>
                  {variablesB.map((_, idx) => (
                    <React.Fragment key={idx}>
                      <th className="p-2 font-semibold border">Value</th>
                      <th className="p-2 font-semibold border">Std</th>
                    </React.Fragment>
                  ))}
                </tr>
              </thead>
              <tbody>
                {scenarios.map((scenario, sIdx) => (
                  <tr key={scenario}>
                    <td className="p-2 font-semibold border">{scenario}</td>
                    {variablesB.map((v, vIdx) => {
                      const scenarioVal = scenarioValuesB[sIdx]?.[vIdx] || "";
                      const inputVal = parseNumber(scenarioVal);
                      const minVal = parseNumber(v.min);
                      const maxVal = parseNumber(v.max);
                      const stdNum = isNaN(inputVal) || isNaN(minVal) || isNaN(maxVal) || maxVal === minVal
                        ? 0
                        : (inputVal - minVal) / (maxVal - minVal);
                      const std = isNaN(inputVal) || isNaN(minVal) || isNaN(maxVal) || maxVal === minVal
                        ? ""
                        : stdNum.toFixed(2);
                      return (
                        <React.Fragment key={vIdx}>
                          <td className="p-2 border text-center">
                            <input
                              type="text"
                              className="w-16 px-1 py-0.5 border rounded"
                              value={scenarioVal}
                              onChange={e => handleScenarioChangeB(sIdx, vIdx, e.target.value)}
                              placeholder="Value"
                            />
                          </td>
                          <td className="p-2 border text-center">
                            {std}
                          </td>
                        </React.Fragment>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-8">
            <h4 className="font-semibold mb-2">Payoff Formula</h4>
            <div className="flex items-center gap-2 mb-2">
              <label htmlFor="formulaB" className="font-mono text-xs">Formula:</label>
              <input
                id="formulaB"
                type="text"
                className="w-full max-w-md px-2 py-1 border rounded font-mono text-xs"
                value={formulaB}
                onChange={e => setFormulaB(e.target.value)}
                placeholder="e.g. (v1_Stnd*0.2)+(v2_Stnd*0.2)+(v3_Stnd*0.4)+(v4_Stnd*0.1)+(v5_Stnd*0.1)"
              />
            </div>
            <table className="min-w-[300px] border border-gray-200 rounded-lg text-xs sm:text-sm">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 font-semibold border">Scenario</th>
                  <th className="p-2 font-semibold border">Payoff Formula Result</th>
                </tr>
              </thead>
              <tbody>
                {scenarios.map((scenario, sIdx) => {
                  // Build variable map: v1_Stnd, v2_Stnd, ... and v1_Val, v2_Val, ...
                  const vars: Record<string, number> = {};
                  variablesB.forEach((v, vIdx) => {
                    const inputVal = parseNumber(scenarioValuesB[sIdx]?.[vIdx] || "");
                    const stdNum = isNaN(inputVal) || isNaN(parseNumber(v.min)) || isNaN(parseNumber(v.max)) || parseNumber(v.max) === parseNumber(v.min)
                      ? 0
                      : (inputVal - parseNumber(v.min)) / (parseNumber(v.max) - parseNumber(v.min));
                    vars[`v${vIdx + 1}_Stnd`] = stdNum;
                    vars[`v${vIdx + 1}_Val`] = isNaN(inputVal) ? 0 : inputVal;
                    vars[`v${vIdx + 1}_mean`] = isNaN(parseNumber(v.mean)) ? 0 : parseNumber(v.mean);
                    vars[`v${vIdx + 1}_max`] = isNaN(parseNumber(v.max)) ? 0 : parseNumber(v.max);
                    vars[`v${vIdx + 1}_min`] = isNaN(parseNumber(v.min)) ? 0 : parseNumber(v.min);
                    vars[`v${vIdx + 1}_weight`] = isNaN(parseNumber(v.weight)) ? 0 : parseNumber(v.weight);
                  });
                  const result = formulaB ? safeEval(formulaB, vars) : "";
                  return (
                    <tr key={scenario}>
                      <td className="p-2 border font-semibold">{scenario}</td>
                      <td className="p-2 border text-right">{result !== "" ? Number(result).toFixed(4) : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
      <div className="w-full max-w-4xl mt-12 flex flex-col items-center">
        <button
          type="button"
          className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors font-semibold text-base"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit"}
        </button>
        {error && <div className="mt-4 text-red-600 font-mono">Error: {error}</div>}
        {apiResponse && (
          <pre className="mt-4 w-full bg-gray-100 dark:bg-gray-900 p-4 rounded text-xs overflow-x-auto text-left">
            {apiResponse}
          </pre>
        )}
      </div>
    </div>
  );
}
