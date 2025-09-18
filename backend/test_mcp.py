#!/usr/bin/env python3
"""Test MCP server communication."""
import subprocess
import json
import sys
import time

def send_message(proc, message):
    """Send a JSON-RPC message to the MCP server."""
    msg_str = json.dumps(message)
    proc.stdin.write(msg_str + '\n')
    proc.stdin.flush()

    # Try to read response
    response_line = proc.stdout.readline()
    if response_line:
        return json.loads(response_line)
    return None

def test_mcp_server():
    """Test the MCP server initialization sequence."""
    print("Starting MCP server test...")

    # Start the MCP server
    proc = subprocess.Popen(
        ['poetry', 'run', 'python', 'scripts/run_mcp_products.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd='/home/rubenayla/repos/partle/backend'
    )

    try:
        # Wait a bit for startup
        time.sleep(0.5)

        # Send initialize request
        print("\n1. Sending initialize request...")
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0.0",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "id": 1
        }

        response = send_message(proc, init_msg)
        if response:
            print(f"✓ Got response: {json.dumps(response, indent=2)}")

            # Check for errors
            if 'error' in response:
                print(f"✗ Error in response: {response['error']}")
                return False

            # Send tools/list request
            print("\n2. Sending tools/list request...")
            list_msg = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 2
            }

            response = send_message(proc, list_msg)
            if response:
                print(f"✓ Got tools response: {json.dumps(response, indent=2)[:500]}...")

                if 'result' in response and 'tools' in response['result']:
                    print(f"\n✓ Found {len(response['result']['tools'])} tools")
                    for tool in response['result']['tools'][:3]:
                        print(f"  - {tool['name']}: {tool['description'][:60]}...")
                    return True
            else:
                print("✗ No response to tools/list")
        else:
            print("✗ No response to initialize")

            # Check stderr for errors
            stderr_output = proc.stderr.read()
            if stderr_output:
                print(f"\nStderr output:\n{stderr_output}")

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False
    finally:
        proc.terminate()
        proc.wait(timeout=2)

    return False

if __name__ == '__main__':
    success = test_mcp_server()
    sys.exit(0 if success else 1)