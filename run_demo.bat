@echo off
title DAA Capstone - CLI Demonstration & Benchmarking
echo =======================================================================
echo   DAA CAPSTONE: INTELLIGENT COURIER PLANNING SYSTEM
echo   Running End-to-End Terminal Demonstration (Phases 1-5)...
echo =======================================================================
python main.py --demo
echo.
echo Running Unit Test Suite...
python -m unittest discover tests
echo.
pause

