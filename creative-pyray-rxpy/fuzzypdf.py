#!/usr/bin/env python3
"""
PDF Search Application - Python Port
A file search application for PDF files with specific naming patterns.
"""

import os
import sys
import subprocess
import shlex
from typing import Optional, List, NamedTuple
from dataclasses import dataclass
from pathlib import Path
import pyray as rl

# --- Configuration ---
PDF_DIRECTORY = "/media/naranyala/Data/OLAHMARKDOWN-vault-work/"
FILE_PREFIX = "__"  # Double underscore requirement
FILE_EXTENSION = ".pdf"
MAX_RESULTS = 10
FONT_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_QUERY_LENGTH = 100
FLOAT_EPSILON = 1e-9
MAX_SCAN_DEPTH = 3

# --- Core Types ---
class NonEmptyString:
    def __init__(self, value: str):
        if not value:
            raise ValueError("String cannot be empty")
        self._value = value
    
    def __str__(self) -> str:
        return self._value
    
    def __repr__(self) -> str:
        return f"NonEmptyString('{self._value}')"

class Score:
    def __init__(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("Score must be between 0.0 and 1.0")
        self._value = value
    
    def __float__(self) -> float:
        return self._value
    
    def __str__(self) -> str:
        return str(self._value)

ValidIndex = int  # Natural numbers (>= 0)
ScanDepth = int   # Range 0 to MAX_SCAN_DEPTH

@dataclass
class PdfFile:
    full_path: NonEmptyString
    file_name: NonEmptyString
    relative_path: NonEmptyString
    match_score: Score
    depth: ScanDepth

@dataclass
class AppState:
    search_query: str
    available_files: List[NonEmptyString]
    filtered_results: List[PdfFile]
    selected_index: ValidIndex
    requires_update: bool
    base_directory: NonEmptyString

# --- Type Constructors and Validators ---
def to_non_empty_string(s: str) -> Optional[NonEmptyString]:
    try:
        return NonEmptyString(s) if s else None
    except ValueError:
        return None

def to_score(value: float) -> Optional[Score]:
    try:
        return Score(value) if 0.0 <= value <= 1.0 else None
    except ValueError:
        return None

def to_scan_depth(depth: int) -> Optional[ScanDepth]:
    return depth if 0 <= depth <= MAX_SCAN_DEPTH else None

# --- Utility Functions ---
def log_error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)

def log_debug(msg: str) -> None:
    print(f"DEBUG: {msg}", file=sys.stderr)

def escape_shell_argument(arg: NonEmptyString) -> str:
    return shlex.quote(str(arg))

def is_valid_pdf_file(file_path: str) -> bool:
    """Check if file is a valid PDF file matching our criteria"""
    try:
        if not os.path.isfile(file_path):
            return False
        
        name = os.path.basename(file_path)
        is_valid_prefix = name.startswith(FILE_PREFIX)
        is_valid_extension = name.endswith(FILE_EXTENSION)
        has_valid_length = len(name) > (len(FILE_PREFIX) + len(FILE_EXTENSION))
        
        is_valid = is_valid_prefix and is_valid_extension and has_valid_length
        
        if is_valid:
            log_debug(f"Valid PDF found: {name}")
        
        return is_valid
    except OSError as e:
        log_error(f"Failed to validate file {file_path}: {e}")
        return False

def calculate_relative_path(full_path: NonEmptyString, base_dir: NonEmptyString) -> Optional[NonEmptyString]:
    full_path_str = str(full_path)
    base_dir_str = str(base_dir)
    
    try:
        full_path_resolved = os.path.abspath(full_path_str)
        base_dir_resolved = os.path.abspath(base_dir_str)
        
        if full_path_resolved.startswith(base_dir_resolved):
            relative_part = full_path_resolved[len(base_dir_resolved):]
            clean_relative = relative_part.lstrip(os.sep)
            return to_non_empty_string(clean_relative)
        else:
            return to_non_empty_string(os.path.basename(full_path_str))
    except OSError as e:
        log_error(f"Failed to calculate relative path for {full_path}: {e}")
        return to_non_empty_string(os.path.basename(str(full_path)))

def calculate_directory_depth(file_path: str, base_dir: str) -> ScanDepth:
    """Calculate directory depth relative to base directory"""
    try:
        normalized_file = os.path.abspath(file_path)
        normalized_base = os.path.abspath(base_dir)
        
        if not normalized_file.startswith(normalized_base):
            return 0
        
        relative_path = normalized_file[len(normalized_base):]
        path_components = [c for c in relative_path.split(os.sep) if c]
        
        # Subtract 1 because the last component is the filename
        dir_depth = max(0, len(path_components) - 1)
        valid_depth = to_scan_depth(dir_depth)
        
        if valid_depth is not None:
            return valid_depth
        else:
            log_error(f"Directory depth {dir_depth} exceeds maximum {MAX_SCAN_DEPTH}")
            return MAX_SCAN_DEPTH
    except OSError as e:
        log_error(f"Failed to calculate depth for {file_path}: {e}")
        return 0

def scan_recursive(current_path: str, current_depth: ScanDepth, max_depth: ScanDepth, base_dir: str) -> List[PdfFile]:
    """Recursively scan directory for PDF files"""
    result = []
    
    log_debug(f"Scanning directory: {current_path} at depth {current_depth}/{max_depth}")
    
    if current_depth > max_depth:
        log_debug(f"Stopping scan at depth {current_depth} (exceeds max {max_depth})")
        return result
    
    if not os.path.isdir(current_path):
        log_error(f"Directory {current_path} does not exist")
        return result
    
    try:
        file_count = 0
        dir_count = 0
        
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            
            if os.path.isfile(entry_path):
                file_count += 1
                if is_valid_pdf_file(entry_path):
                    full_path_opt = to_non_empty_string(entry_path)
                    base_dir_opt = to_non_empty_string(base_dir)
                    
                    if full_path_opt and base_dir_opt:
                        relative_path = calculate_relative_path(full_path_opt, base_dir_opt)
                        file_name = to_non_empty_string(os.path.basename(entry_path))
                        file_depth = calculate_directory_depth(entry_path, base_dir)
                        
                        if relative_path and file_name:
                            log_debug(f"Found valid PDF: {file_name} at depth {file_depth}")
                            result.append(PdfFile(
                                full_path=full_path_opt,
                                file_name=file_name,
                                relative_path=relative_path,
                                match_score=Score(1.0),
                                depth=file_depth
                            ))
                        else:
                            log_error(f"Failed to process file paths for: {entry_path}")
                    else:
                        log_error(f"Failed to convert paths to NonEmptyString: {entry_path}")
            
            elif os.path.isdir(entry_path):
                dir_count += 1
                if current_depth < max_depth:
                    next_depth = current_depth + 1
                    if to_scan_depth(next_depth) is not None:
                        log_debug(f"Recursing into: {entry_path} at depth {next_depth}")
                        sub_results = scan_recursive(entry_path, next_depth, max_depth, base_dir)
                        log_debug(f"Found {len(sub_results)} PDFs in subdirectory: {entry_path}")
                        result.extend(sub_results)
                    else:
                        log_error(f"Cannot increment depth beyond maximum: {current_depth}")
                else:
                    log_debug(f"Skipping subdirectory {entry_path} (at max depth {max_depth})")
        
        log_debug(f"Scanned {file_count} files and {dir_count} directories at {current_path}")
        log_debug(f"Found {len(result)} valid PDFs at depth {current_depth}")
    
    except OSError as e:
        log_error(f"Failed to scan directory {current_path} at depth {current_depth}: {e}")
    
    return result

def scan_pdf_directory_recursive(dir_path: NonEmptyString, max_depth: ScanDepth) -> List[PdfFile]:
    """Recursively scan directory for valid PDF files up to specified depth"""
    log_debug(f"Starting recursive scan of {dir_path} with max depth {max_depth}")
    result = scan_recursive(str(dir_path), 0, max_depth, str(dir_path))
    log_debug(f"Total PDFs found in recursive scan: {len(result)}")
    return result

def scan_pdf_directory(dir_path: NonEmptyString) -> List[NonEmptyString]:
    """Wrapper function to maintain compatibility with existing code"""
    pdf_files = scan_pdf_directory_recursive(dir_path, MAX_SCAN_DEPTH)
    result = [pdf_file.full_path for pdf_file in pdf_files]
    log_debug(f"scan_pdf_directory returning {len(result)} file paths")
    return result

def calculate_match_score(file_name: str, query: str) -> Optional[Score]:
    """Calculate match score between filename and query"""
    if not file_name:
        log_error("calculate_match_score: file_name cannot be empty")
        return None
    
    if not query:
        return to_score(1.0)
    
    file_name_lower = file_name.lower()
    query_lower = query.lower()
    
    query_idx = 0
    match_positions = []
    
    for i, ch in enumerate(file_name_lower):
        if query_idx < len(query_lower) and ch == query_lower[query_idx]:
            match_positions.append(i)
            query_idx += 1
    
    if query_idx != len(query_lower):
        return None
    
    if len(file_name_lower) == 0:
        log_error("calculate_match_score: file_name_lower has zero length")
        return None
    
    match_ratio = len(query_lower) / len(file_name_lower)
    early_bonus = (1.0 - (match_positions[0] / len(file_name_lower))) if match_positions else 0.0
    
    final_score = match_ratio * 0.6 + early_bonus * 0.4
    return to_score(final_score)

def filter_and_score_files(all_files: List[NonEmptyString], query: str, base_dir: NonEmptyString) -> List[PdfFile]:
    """Filter and score files based on query"""
    result = []
    
    log_debug(f"Filtering {len(all_files)} files with query: '{query}'")
    
    for file_path in all_files:
        file_name = to_non_empty_string(os.path.basename(str(file_path)))
        if not file_name:
            log_error(f"Failed to extract filename from: {file_path}")
            continue
        
        file_name_score = calculate_match_score(str(file_name), query)
        relative_path = calculate_relative_path(file_path, base_dir)
        
        final_score = None
        
        if file_name_score:
            final_score = file_name_score
        elif relative_path:
            path_score = calculate_match_score(str(relative_path), query)
            if path_score:
                final_score = to_score(float(path_score) * 0.8)
        
        if final_score and relative_path:
            file_depth = calculate_directory_depth(str(file_path), str(base_dir))
            
            result.append(PdfFile(
                full_path=file_path,
                file_name=file_name,
                relative_path=relative_path,
                match_score=final_score,
                depth=file_depth
            ))
    
    # Sort results
    def sort_key(pdf_file):
        score_val = float(pdf_file.match_score)
        depth_val = pdf_file.depth
        path_val = str(pdf_file.relative_path)
        return (-score_val, depth_val, path_val)  # Negative score for descending order
    
    result.sort(key=sort_key)
    
    if len(result) > MAX_RESULTS:
        result = result[:MAX_RESULTS]
    
    log_debug(f"Filtered results: {len(result)} files")
    return result

def open_file(file_path: NonEmptyString) -> bool:
    """Open file with system default application"""
    if not os.path.isfile(str(file_path)):
        log_error(f"File {file_path} does not exist")
        return False
    
    try:
        command = ["xdg-open", str(file_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            log_error(f"Failed to open file {file_path}: exit code {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        log_error(f"Failed to open file {file_path}: {e}")
        return False

# --- Input Handling ---
def is_printable_ascii(ch: str) -> bool:
    """Check if character is printable ASCII"""
    return len(ch) == 1 and 32 <= ord(ch) <= 126

def is_valid_input_character(char_code: int) -> bool:
    """Check if character code represents a valid input character"""
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -.,_/")
    
    if char_code < 0 or char_code > 127:
        return False
    
    ch = chr(char_code)
    return is_printable_ascii(ch) and ch in allowed_chars

def handle_keyboard_input(state: AppState) -> None:
    """Handle keyboard input for the application"""
    # Handle character input
    ch = rl.get_char_pressed()
    while ch != 0:
        if len(state.search_query) < MAX_QUERY_LENGTH and is_valid_input_character(ch):
            state.search_query += chr(ch)
            state.selected_index = 0
            state.requires_update = True
        elif len(state.search_query) >= MAX_QUERY_LENGTH:
            log_error(f"Query length limit reached: {MAX_QUERY_LENGTH}")
        ch = rl.get_char_pressed()
    
    # Handle backspace
    if rl.is_key_pressed(rl.KeyboardKey.KEY_BACKSPACE) and len(state.search_query) > 0:
        state.search_query = state.search_query[:-1]
        state.selected_index = 0
        state.requires_update = True
    
    # Handle navigation
    if state.filtered_results:
        max_idx = len(state.filtered_results) - 1
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_DOWN) and state.selected_index < max_idx:
            state.selected_index += 1
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_UP) and state.selected_index > 0:
            state.selected_index -= 1
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_PAGE_DOWN):
            state.selected_index = min(max_idx, state.selected_index + 5)
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_PAGE_UP):
            state.selected_index = max(0, state.selected_index - 5)
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_HOME):
            state.selected_index = 0
        
        if rl.is_key_pressed(rl.KeyboardKey.KEY_END):
            state.selected_index = max_idx
        
        # Handle file opening
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
            if state.selected_index < len(state.filtered_results):
                selected_file = state.filtered_results[state.selected_index]
                success = open_file(selected_file.full_path)
                if not success:
                    log_error(f"Failed to open selected file: {selected_file.full_path}")
            else:
                log_error(f"Invalid selection index: {state.selected_index}")
    else:
        state.selected_index = 0
    
    # Handle escape key
    if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        state.search_query = ""
        state.selected_index = 0
        state.requires_update = True

# --- Rendering ---
def is_render_position_valid(y_pos: int) -> bool:
    """Check if render position is valid"""
    return 0 <= y_pos < WINDOW_HEIGHT

def draw_interface(state: AppState) -> None:
    """Draw the application interface"""
    MARGIN = 10
    LINE_HEIGHT = FONT_SIZE + 4
    
    rl.clear_background(rl.RAYWHITE)
    
    # Draw query input
    query_display = f"Query: {state.search_query}_"
    rl.draw_text(query_display, MARGIN, MARGIN, FONT_SIZE, rl.DARKGRAY)
    
    # Draw help text
    help_text = f"ESC: Clear | Enter: Open | ↑↓: Navigate | Only shows '{FILE_PREFIX}*.pdf' files"
    rl.draw_text(help_text, MARGIN, MARGIN + LINE_HEIGHT, 14, rl.GRAY)
    
    # Draw count text
    count_text = f"Results: {len(state.filtered_results)} (scanning depth 0-{MAX_SCAN_DEPTH})"
    rl.draw_text(count_text, MARGIN, MARGIN + LINE_HEIGHT * 2, 14, rl.GRAY)
    
    # Draw results
    results_start_y = MARGIN + LINE_HEIGHT * 3 + 10
    
    for i, pdf_file in enumerate(state.filtered_results):
        y_pos = results_start_y + i * LINE_HEIGHT
        is_selected = i == state.selected_index
        
        if not is_render_position_valid(y_pos) or y_pos >= WINDOW_HEIGHT - LINE_HEIGHT:
            if is_selected:
                log_error(f"Selected item {i} is off-screen at Y position {y_pos}")
            continue
        
        # Draw selection background
        if is_selected:
            rect_width = WINDOW_WIDTH - MARGIN * 2
            selection_color = rl.Color(240, 240, 240, 255)
            rl.draw_rectangle(
                MARGIN - 2,
                y_pos - 2,
                rect_width,
                LINE_HEIGHT,
                selection_color
            )
        
        # Draw file entry
        prefix = "▶ " if is_selected else "  "
        depth_indicator = "│ " * pdf_file.depth
        display_text = f"{prefix}{depth_indicator}{pdf_file.relative_path}"
        text_color = rl.RED if is_selected else rl.BLACK
        
        rl.draw_text(display_text, MARGIN, y_pos, FONT_SIZE, text_color)
        
        # Draw score and depth info for selected item
        if is_selected:
            score_text = f"Score: {float(pdf_file.match_score):.3f} Depth: {pdf_file.depth}"
            score_x_pos = WINDOW_WIDTH - 200
            rl.draw_text(score_text, score_x_pos, y_pos, 12, rl.BLUE)

# --- Application Lifecycle ---
def initialize_app() -> AppState:
    """Initialize the application state"""
    dir_path = PDF_DIRECTORY if PDF_DIRECTORY else os.getcwd()
    dir_obj = to_non_empty_string(dir_path)
    
    if not dir_obj:
        log_error(f"Failed to create valid directory path from: {dir_path}")
        return AppState(
            search_query="",
            available_files=[],
            filtered_results=[],
            selected_index=0,
            requires_update=True,
            base_directory=to_non_empty_string(".")  # Fallback
        )
    
    log_debug(f"Initializing app with directory: {dir_path}")
    log_debug(f"Looking for files with prefix '{FILE_PREFIX}' and extension '{FILE_EXTENSION}'")
    
    available_files = scan_pdf_directory(dir_obj)
    if not available_files:
        log_error(f"No valid PDF files found in directory tree: {dir_path}")
        log_error(f"Looking for files matching pattern: {FILE_PREFIX}*{FILE_EXTENSION}")
    else:
        log_debug(f"Found {len(available_files)} PDF files matching pattern '{FILE_PREFIX}*{FILE_EXTENSION}'")
    
    return AppState(
        search_query="",
        available_files=available_files,
        filtered_results=[],
        selected_index=0,
        requires_update=True,
        base_directory=dir_obj
    )

def update_app(state: AppState) -> None:
    """Update application state"""
    if state.requires_update:
        trimmed_query = state.search_query.strip()
        state.filtered_results = filter_and_score_files(state.available_files, trimmed_query, state.base_directory)
        
        if state.filtered_results:
            state.selected_index = min(state.selected_index, len(state.filtered_results) - 1)
        else:
            state.selected_index = 0
        
        state.requires_update = False

def run_main_loop() -> None:
    """Run the main application loop"""
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, f"PDF Search - '{FILE_PREFIX}*.pdf' files")
    rl.set_target_fps(60)
    
    app_state = initialize_app()
    
    if not app_state.available_files:
        log_error(f"Warning: No PDF files with prefix '{FILE_PREFIX}' found for searching")
    
    while not rl.window_should_close():
        try:
            handle_keyboard_input(app_state)
            update_app(app_state)
            
            rl.begin_drawing()
            draw_interface(app_state)
            rl.end_drawing()
        except Exception as e:
            log_error(f"Runtime error in main loop: {e}")
    
    rl.close_window()

def main() -> None:
    """Main entry point"""
    try:
        run_main_loop()
    except Exception as e:
        log_error(f"Fatal error in main: {e}")
        print("Application terminated due to fatal error", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
