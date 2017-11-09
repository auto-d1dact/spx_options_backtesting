
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyUI(fluidPage(

  # Application title
  titlePanel("SPX Option Tester"),

  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(
      sliderInput("dte",
                  "Days to Expiry:",
                  min = 1,
                  max = 90,
                  value = 30),
      numericInput("var", "VaR Percent:", 0.005)
    ),

    # Show a plot of the generated distribution
    mainPanel(
      #plotOutput("distPlot")
    )
  )
))
