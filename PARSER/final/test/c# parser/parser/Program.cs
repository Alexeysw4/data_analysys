using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace parser
{
    class Program
    {
        static void Main(string[] args)
        { 
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            Encoding.GetEncoding("windows-1254");

            var parser = new Parser();
        }
    }
}
