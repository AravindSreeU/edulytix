from edulib import main, gemini_summary, compose, clear

try:
    main.run()
    gemini_summary.run()
    compose.run()
    
finally:
    clear.run()
