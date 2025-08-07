using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace project01
{
    internal class Program
    {
        static void Main(string[] args)
        {
            /*int age = 19;
            string name = "sihanas";
            double height = 140.2;

            Console.WriteLine("Hi.");
            Console.WriteLine("I am " + name + ". I am " + age); */

            /*
            int a = 25;
            int b = 27; 

            Console.WriteLine("Addition: " + (a + b));
            Console.WriteLine("Subtraction: " + (a - b));
            Console.WriteLine("Multiplication: " + (a * b));
            Console.WriteLine("Division: " + (a / b));
            Console.WriteLine("Modulus: " + (b % a));

            a++;
            Console.WriteLine("Increment: " + a);

            b--;
            Console.WriteLine("Decrement: " + b); 
            */

            /*
            Console.WriteLine("Enter your user_name");
            string UserName = Console.ReadLine();

            if (UserName == "Sihanas")
            {
                Console.WriteLine("You are an user!");
            }

            else if (UserName == "Admin")
            {
                Console.WriteLine("You are an Admin!");
            }

            else
            {
                Console.WriteLine("Invalid User!!");
            }
            */

            Console.WriteLine("Enter your score: ");
            int Score = Int32.Parse(Console.ReadLine());

            if (Score >= 75)
            {
                Console.WriteLine("You scored A");
            }

            else if (Score >= 65)
            {
                Console.WriteLine("You scored B");
            }

            else if (Score >= 55)
            {
                Console.WriteLine("You scored C");
            }

            else
            {
                Console.WriteLine("You scored F");
            }

        }
    }
}
