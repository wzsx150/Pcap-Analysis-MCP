# -*- coding: utf-8 -*-
"""
MCP Protocol Handler

Implements the Model Context Protocol (MCP) for stdio transport.
"""

import sys
import json
from typing import Any, Dict, Optional


class MCPProtocol:
    """Simple MCP stdio protocol handler for JSON-RPC communication."""
    
    @staticmethod
    def read_message() -> Optional[Dict]:
        """
        Read a JSON-RPC message from stdin.
        
        Returns:
            Parsed JSON dict or None if read fails/EOF.
        """
        try:
            line = sys.stdin.readline()
            if not line:
                return None
            return json.loads(line.strip())
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    @staticmethod
    def write_message(msg: Dict) -> None:
        """
        Write a JSON-RPC message to stdout.
        
        Args:
            msg: Message dictionary to serialize and write.
        """
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()
    
    @staticmethod
    def success_response(req_id: Any, result: Any) -> Dict:
        """
        Create a JSON-RPC success response.
        
        Args:
            req_id: Request ID to echo back.
            result: Result payload.
            
        Returns:
            JSON-RPC response dict.
        """
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }
    
    @staticmethod
    def error_response(req_id: Any, code: int, message: str, data: Any = None) -> Dict:
        """
        Create a JSON-RPC error response.
        
        Args:
            req_id: Request ID to echo back.
            code: Error code (negative for JSON-RPC errors).
            message: Human-readable error message.
            data: Optional additional error data.
            
        Returns:
            JSON-RPC error response dict.
        """
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": error
        }
    
    @staticmethod
    def notification(method: str, params: Dict = None) -> Dict:
        """
        Create a JSON-RPC notification (no id, no response expected).
        
        Args:
            method: Method name.
            params: Optional parameters.
            
        Returns:
            JSON-RPC notification dict.
        """
        msg = {"jsonrpc": "2.0", "method": method}
        if params:
            msg["params"] = params
        return msg

