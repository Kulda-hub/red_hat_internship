using System;
using System.Collections.Generic;
using System.Linq;

namespace MenuScrapper
{
    //TODO: Create console UI and all 6 (5 + search) methods from pdf.
    public class MenuHandler
    {
        public Scrapper Restaurants { get; set; }

        public MenuHandler(Scrapper restaurants)
        {
            this.Restaurants = restaurants;
            PrintOptions();
            bool done = false;
            while (!done)
            {
                var key = Console.ReadKey().KeyChar;
                Console.Clear();
                switch (key)
                {
                    case '1':
                        PrintTodayAll();
                        PrintOptions();
                        break;
                    case '2':
                        PrintTodayRestaurant();
                        PrintOptions();
                        break;
                    case '3':
                        PrintDayAll();
                        PrintOptions();
                        break;
                    case '4':
                        PrintDayRestaurant();
                        PrintOptions();
                        break;
                    case '5':
                        PrintAll();
                        PrintOptions();
                        break;
                    case '6':
                        Search();
                        PrintOptions();
                        break;
                    case '7':
                        done = true;
                        break;
                    default:
                        PrintOptions();
                        break;
                }
            }
        }

        private void PrintDayRestaurant()
        {
            PrintOptionsDays();
            var key = Console.ReadKey().KeyChar;
            DayOfWeek day;
            Console.WriteLine();
            switch (key)
            {
                case '1':
                    day = DayOfWeek.Monday;
                    break;
                case '2':
                    day = DayOfWeek.Tuesday;
                    break;
                case '3':
                    day = DayOfWeek.Wednesday;
                    break;
                case '4':
                    day = DayOfWeek.Thursday;
                    break;
                case '5':
                    day = DayOfWeek.Friday;
                    break;
                default:
                    return;
            }
            PrintOptionsRestaurants();
            key = Console.ReadKey().KeyChar;
            Console.WriteLine();
            switch (key)
            {
                case '1':
                    PrintRestaurantDaymenu(Restaurants.AlCapone, day);
                    break;
                case '2':
                    PrintRestaurantDaymenu(Restaurants.UDrevaka, day);
                    break;
                case '3':
                    PrintRestaurantDaymenu(Restaurants.UCapa, day);
                    break;
                default:
                    return;
            }

        }

        private void PrintTodayRestaurant()
        {
            PrintOptionsRestaurants();
            var key = Console.ReadKey().KeyChar;
            Console.WriteLine();
            switch (key)
            {
                case '1':
                    PrintRestaurantDaymenu(Restaurants.AlCapone, DateTime.Now.DayOfWeek);
                    break;
                case '2':
                    PrintRestaurantDaymenu(Restaurants.UDrevaka, DateTime.Now.DayOfWeek);
                    break;
                case '3':
                    PrintRestaurantDaymenu(Restaurants.UCapa, DateTime.Now.DayOfWeek);
                    break;
                default:
                    return;
            }
        }

        private void PrintDayAll()
        {
            Console.WriteLine();
            PrintOptionsDays();
            var key = Console.ReadKey().KeyChar;
            Console.WriteLine();
            DayOfWeek day;
            switch (key)
            {
                case '1':
                    day = DayOfWeek.Monday;
                    break;
                case '2':
                    day = DayOfWeek.Tuesday;
                    break;
                case '3':
                    day = DayOfWeek.Wednesday;
                    break;
                case '4':
                    day = DayOfWeek.Thursday;
                    break;
                case '5':
                    day = DayOfWeek.Friday;
                    break;
                default:
                    return;
            }
            PrintRestaurantDaymenu(Restaurants.AlCapone, day);
            PrintRestaurantDaymenu(Restaurants.UDrevaka, day);
            PrintRestaurantDaymenu(Restaurants.UCapa, day);
        }
        private void PrintTodayAll()
        {
            Console.WriteLine();
            PrintRestaurantDaymenu(Restaurants.AlCapone, DateTime.Now.DayOfWeek);
            PrintRestaurantDaymenu(Restaurants.UDrevaka, DateTime.Now.DayOfWeek);
            PrintRestaurantDaymenu(Restaurants.UCapa, DateTime.Now.DayOfWeek);
        }
        
        private static void PrintRestaurantDaymenu(Tuple<string, List<DayMenu>> restaurant, DayOfWeek day)
        {
            Console.WriteLine();
            bool found = false;
            foreach (var dayMenu in restaurant.Item2
                .Where(dayMenu => Utils.IsSameDay(day, dayMenu.Day)))
            {
                found = true;
                Console.WriteLine(restaurant.Item1);
                Console.WriteLine(dayMenu);
            }
            if (!found)
            {
                Console.WriteLine("There is no menu for {0} in {1} ", day, restaurant.Item1);
            }
        }

        private static void PrintOptions()
        {
            Console.WriteLine();
            Console.WriteLine("1 - Print today‘s menu for all restaurants");
            Console.WriteLine("2 - Print today‘s menu for restaurant ");
            Console.WriteLine("3 - Print menu for all restaurants by day ");
            Console.WriteLine("4 - Print menu for restaurant by day ");
            Console.WriteLine("5 - Print week menu for all restaurants ");
            Console.WriteLine("6 - Search");
            Console.WriteLine("7 - Quit");
            Console.WriteLine("//Select option from <1,7>:");
        }

        private void PrintOptionsDays()
        {
            Console.WriteLine();
            Console.WriteLine("1 - Monday");
            Console.WriteLine("2 - Tuesday");
            Console.WriteLine("3 - Wednesday");
            Console.WriteLine("4 - Thursday");
            Console.WriteLine("5 - Friday");
            Console.WriteLine("//Select option from <1,5>");
        }

        private void PrintOptionsRestaurants()
        {
            Console.WriteLine();
            Console.WriteLine("1 - Al Capone - Pizzeria Ristorante ");
            Console.WriteLine("2 - U Dřeváka Beer & Grill");
            Console.WriteLine("3 - Pivnice u Čápa");
            Console.WriteLine("//Select option from <1,3>: ");
        }

        private void PrintAll()
        {
            Console.WriteLine();
            PrintRestaurant(Restaurants.AlCapone);
            PrintRestaurant(Restaurants.UDrevaka);
            PrintRestaurant(Restaurants.UCapa);
        }

        private static void PrintRestaurant(Tuple<string, List<DayMenu>> restaurant)
        {
            Console.WriteLine(restaurant.Item1);
            foreach (var day in restaurant.Item2)
            {
                Console.WriteLine(day);
            }
        }

        private void Search()
        {
            Console.WriteLine();
            Console.WriteLine("Search the menu:");
            string target = Console.ReadLine();
            if (target == null)
            {
                return;
            }
            SearchRestaurant(Restaurants.AlCapone, target);
            SearchRestaurant(Restaurants.UDrevaka, target);
            SearchRestaurant(Restaurants.UCapa, target);
        }

        private void SearchRestaurant(Tuple<string, List<DayMenu>> restaurant, string target)
        {
            bool found = false;
            foreach (var dayMenu in restaurant.Item2
                .Where(dayMenu => dayMenu.Meals.Any(meal => meal.Name.Contains(target))))
            {
                if (!found)
                {
                    Console.WriteLine(restaurant.Item1);
                    found = true;
                }
                Console.WriteLine(dayMenu);
            }
            if (!found)
            {
                Console.WriteLine("The food you are looking for is not in {0} ", restaurant.Item1);
            }
        }
    }
}
