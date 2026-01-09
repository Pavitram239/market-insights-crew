from dotenv import load_dotenv
from crew import stock_crew
import argparse
import json
from typing import List

load_dotenv()

def save_results(results: dict, filename: str):
    """Save analysis results to a file"""
    try:
        if filename.endswith('.json'):
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            with open(filename, 'w') as f:
                for stock, result in results.items():
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Stock: {stock}\n")
                    f.write(f"{'='*60}\n")
                    f.write(f"{result}\n")
        
        print(f"\n✅ Results saved to: {filename}")
    except Exception as e:
        print(f"\n❌ Error saving results: {str(e)}")

def run(stock: str):
    
    """Analyze a single stock"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {stock}")
    print(f"{'='*60}\n")
    
    result = stock_crew.kickoff(inputs={"stock": stock})
    print(result)
    print(f"\n{'='*60}\n")
    return result

def run_multiple(stocks: List[str], output_file: str = None):
    """Analyze multiple stocks and optionally save results"""
    results = {}
    
    print(f"\nAnalyzing {len(stocks)} stocks: {', '.join(stocks)}\n")
    
    for stock in stocks:
        try:
            result = run(stock)
            results[stock] = str(result)
        except Exception as e:
            print(f"Error analyzing {stock}: {str(e)}")
            results[stock] = f"Error: {str(e)}"
    
    # Save results if output file is specified
    if output_file:
        save_results(results, output_file)
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Stock Analysis with CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single stock
  python main.py --stock AAPL
  
  # Analyze multiple stocks
  python main.py --stocks AAPL MSFT GOOGL
  
  # Analyze stocks from a file
  python main.py --file stocks.txt
  
  # Save results to a file
  python main.py --stocks AAPL TSLA --output results.txt
  
  # Save results as JSON
  python main.py --stocks AAPL TSLA --output results.json
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        '--stock', '-s',
        type=str,
        help='Single stock ticker to analyze (e.g., AAPL)'
    )
    input_group.add_argument(
        '--stocks', '-m',
        nargs='+',
        help='Multiple stock tickers to analyze (e.g., AAPL MSFT GOOGL)'
    )
    input_group.add_argument(
        '--file', '-f',
        type=str,
        help='Path to file containing stock tickers (one per line)'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Save results to file (.txt or .json)'
    )
    
    args = parser.parse_args()
    
    # Determine which stocks to analyze
    stocks_to_analyze = []
    
    if args.stock:
        stocks_to_analyze = [args.stock.upper()]
    elif args.stocks:
        stocks_to_analyze = [s.upper() for s in args.stocks]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                stocks_to_analyze = [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found")
            return
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            return
    else:
        # Default behavior - analyze AAPL
        print("No stock specified. Using default: AAPL")
        print("Use --help for more options\n")
        stocks_to_analyze = ["AAPL"]
    
    # Run analysis
    if len(stocks_to_analyze) == 1:
        run(stocks_to_analyze[0])
    else:
        run_multiple(stocks_to_analyze, args.output)

if __name__ == "__main__":
    main()
