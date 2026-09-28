import sys
import json
from client import BiquadIIRFilterEngine

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-biquad-iir-filter-dsp-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "design_and_filter",
                    "description": "Design a 2nd-order Biquad IIR filter and evaluate signal response",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "filter_type": {"type": "string", "enum": ["lowpass", "highpass", "bandpass", "notch", "peaking"], "default": "lowpass"},
                            "cutoff_freq": {"type": "number", "default": 1000.0},
                            "q_factor": {"type": "number", "default": 0.7071},
                            "gain_db": {"type": "number", "default": 0.0},
                            "freqs": {"type": "array", "items": {"type": "number"}}
                        }
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "design_and_filter":
            engine = BiquadIIRFilterEngine()
            ft = args.get("filter_type", "lowpass")
            cutoff = args.get("cutoff_freq", 1000.0)
            q = args.get("q_factor", 0.7071)
            g = args.get("gain_db", 0.0)
            freqs = args.get("freqs", [100.0, 1000.0, 10000.0])
            coeffs = engine.design_filter(ft, cutoff, q, g)
            bode = engine.frequency_response(coeffs, freqs)
            res = {"content": [{"type": "text", "text": json.dumps({"coefficients": coeffs, "frequency_response": bode})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
