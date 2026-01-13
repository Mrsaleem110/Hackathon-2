"""
Official MCP Server Skills Package
Initialization module for MCP server skills
"""

from .official_server_skills import (
    OfficialMcpSkills,
    get_project_file,
    put_project_file,
    list_project_dir,
    get_sys_info,
    exec_shell_cmd,
    create_proj_structure
)

__all__ = [
    'OfficialMcpSkills',
    'get_project_file',
    'put_project_file',
    'list_project_dir',
    'get_sys_info',
    'exec_shell_cmd',
    'create_proj_structure'
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Official MCP Server"
__description__ = "Skills for interacting with the official MCP server"