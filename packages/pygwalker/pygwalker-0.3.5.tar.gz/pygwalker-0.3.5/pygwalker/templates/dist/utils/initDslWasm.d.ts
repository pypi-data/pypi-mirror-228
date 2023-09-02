import "./wasm_exec.js";
declare global {
    export interface Window {
        Go: any;
    }
}
export declare function initDslToSql(wasmContent: string): Promise<void>;
