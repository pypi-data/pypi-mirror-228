import argparse

from weather_app.utils import WeatherApp

def main():
    li = []
    parser = argparse.ArgumentParser(description="Weather App")
    parser.add_argument("-city", "--city", type = str, default = None, help = "City name", required = True)
    args = parser.parse_args()
    
    if args.city:
        _ = WeatherApp()
        weather = _.get_weather(args.city)
        report = _.weather_report(weather)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()