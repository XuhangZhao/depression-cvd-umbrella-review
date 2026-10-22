# Figure 2: cumulative publication counts through 1 April 2026.
library(ggplot2)
current <- read.csv("data/figure2.csv", check.names = FALSE, stringsAsFactors = FALSE)
stopifnot(all(current$depression_cumulative == cumsum(current$depression_annual)),
          all(current$CVD_cumulative == cumsum(current$CVD_annual)))

plot_data <- rbind(
  data.frame(year = current$year, value = current$depression_cumulative, domain = "Depression"),
  data.frame(year = current$year, value = current$CVD_cumulative, domain = "CVD"))
plot_data$domain <- factor(plot_data$domain, levels = c("Depression", "CVD"))
year_labels <- as.character(2005:2026)
year_labels[length(year_labels)] <- "2026\n(until 1 April)"

figure <- ggplot(plot_data, aes(x = year, y = value, colour = domain, shape = domain, group = domain)) +
  geom_line(linewidth = 0.75) + geom_point(size = 2.0, stroke = 0.45) +
  scale_colour_manual(values = c("Depression" = "#C4846D", "CVD" = "#6B7B8C")) +
  scale_shape_manual(values = c("Depression" = 16, "CVD" = 15)) +
  scale_x_continuous(breaks = 2005:2026, labels = year_labels,
                     expand = expansion(mult = c(0.035, 0.035))) +
  scale_y_continuous(breaks = seq(0, 60, 10), limits = c(-2, 60), expand = c(0, 0)) +
  labs(x = "Publication Year", y = "Cumulative Number of Included Reviews", colour = NULL, shape = NULL) +
  theme_classic(base_family = "Arial", base_size = 7) +
  theme(axis.title.x = element_text(size = 7, colour = "#000000", margin = margin(t = 10)),
        axis.title.y = element_text(size = 7, colour = "#000000", margin = margin(r = 9)),
        axis.text.x = element_text(size = 7, colour = "#000000", angle = 45, hjust = 1, vjust = 1),
        axis.text.y = element_text(size = 7, colour = "#000000"),
        axis.line = element_line(linewidth = 0.5, colour = "black"),
        axis.ticks = element_line(linewidth = 0.5, colour = "black"),
        axis.ticks.length = unit(3.5, "pt"),
        legend.position = "inside", legend.position.inside = c(0.035, 0.965),
        legend.justification = c(0, 1), legend.direction = "vertical",
        legend.text = element_text(size = 7, colour = "#000000"),
        legend.key.width = unit(24, "pt"), legend.key.height = unit(13, "pt"),
        legend.background = element_blank(), plot.margin = margin(13, 5, 7, 5, unit = "mm")) +
  guides(colour = guide_legend(override.aes = list(linewidth = 0.75, size = 2.0)))

if (interactive()) print(figure)
ggsave("figure/Figure_2.png", figure, device = ragg::agg_png,
       width = 180, height = 115, units = "mm", dpi = 600, bg = "white")
