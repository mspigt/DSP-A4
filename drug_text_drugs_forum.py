def free_text(df):
    import glob
    import pandas as pd

    if 'litre/day per 1 000 inhabitants' in df.columns:
        return waste_water_text(df)
    elif 'Percentage of the population' in df.columns:
        return un_drug_report_text(df)  # un_report
    elif 'total' in df.columns:
        return reddit_text(df)
    elif 'percentage_of_post' in df.columns:
        return drug_lab(df)  # emcdda
    elif 'total_drug_forum' in df.columns:
        return drug_forum(df)
    else:
        return print('UNABLE TO CREATE TEXT')


def drug_forum(df):
    sorted_countries = sorted(list(set(df['Country'].tolist())))
    number_countries = len(sorted_countries)

    # return print(sorted_countries)
    number_year = len(set(df['year']))
    sorted_year = sorted(list(set(df['year'])))
    title = ''
    stat = ''

    if number_countries > 3:
        title_fin = "UNABLE TO GENERATE TEXT WHEN THERE IS MORE THAN THREE COUNTRIES SELECTED"
    else:
        if number_countries == 1:
            title = "The country that you have selected is **{}**. ".format(
                sorted_countries[0].capitalize())
            stat = drugs_forum_text(df, number_countries,
                                    sorted_countries, number_year, sorted_year)
        elif number_countries == 2:
            title = "The countries that you have selected are **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize())
            stat = drugs_forum_text(df, number_countries,
                                    sorted_countries, number_year, sorted_year)
        elif number_countries == 3:
            title = "The countries that you have selected are **{}**, **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize(), sorted_countries[2].capitalize())
            stat = drugs_forum_text(df, number_countries,
                                    sorted_countries, number_year, sorted_year)
        if number_year == 1:
            title2 = "The year of interest is **{}**. \n".format(sorted_year[0])
        else:
            title2 = "The selected period is **{} - {}**. \n".format(
                sorted_year[0], sorted_year[-1])
    title_fin = title + "\n" + title2 + "\n" + stat + "\n"
    return title_fin


def drugs_forum_text(df, nc, sc, ny, sy):
    summary_stat = "DrugsForum.nl Analysis:\n\n"

    # single year
    if ny == 1:
        if nc == 1:
            for x in sorted(list(set(df['drug']))):
                measure = str(
                    round(df.loc[df['drug'] == x, 'total_drug_forum'].values[0], 3))
                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                stat = "{} Posts related to **{}**\n".format(
                    measure, drug_name)
                summary_stat += stat + "\n"  # Add a new line here
        else:
            for c in sc:
                summary_stat += "\nCountry: {}\n".format(c.capitalize())
                for x in sorted(list(set(df['drug']))):
                    measure = str(
                        round(df.loc[df['drug'] == x, 'total_drug_forum'].values[0], 3))
                    drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                    stat = "**{}** comments & posts related to {}\n".format(
                        measure, drug_name)
                    summary_stat += stat + "\n"  # Add a new line here
    else:
        # more than one year
        if nc == 1:
            # only one country
            for x in sorted(list(set(df['drug']))):
                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                if len(df.loc[df['drug'] == x]) == 1:
                    period = "{}-{}".format(sy[0], sy[-1])
                    year = str(round(df[(df['drug'] == x) & (
                        (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['year'].values[0], 3))
                    measure_dif = str(round(df[(df['drug'] == x) & (
                        (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['total_drug_forum'].values[0], 3))

                    stat = "There was is only one measurement over the **{}** period for **{}** (**{}**). **{}** comments & posts were flagged.\n".format(
                        period, drug_name, year, measure_dif)
                    summary_stat += stat + "\n"  # Add a new line here

                else:
                    measure1 = round(df.loc[(df['drug'] == x) & (
                        df['year'] == sy[0]), 'total_drug_forum'].values[0], 3)
                    measure2 = round(df.loc[(df['drug'] == x) & (
                        df['year'] == sy[-1]), 'total_drug_forum'].values[0], 3)
                    measure_differ = "{} - {}".format(measure1, measure2)

                    period = "{}-{}".format(sy[0], sy[-1])
                    if measure1 < measure2:
                        direction = "an increase"
                    else:
                        direction = 'a decrease'

                    stat = "There was {} over the {} period for **{}**. **{}** comments & posts were seen.\n".format(direction,
                                                                                                             period,
                                                                                                             drug_name,
                                                                                                             measure_differ)
                    summary_stat += stat + "\n"  # Add a new line here
        else:
            # more than one country
            for c in sc:
                summary_stat += "\nCountry: {}\n".format(c.capitalize())
                for x in sorted(list(set(df['drug']))):
                    drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                    if len(df.loc[df['drug'] == x]) == 1:
                        period = "{}-{}".format(sy[0], sy[-1])
                        year = str(round(df[(df['drug'] == x) & (
                            (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['year'].values[0], 3))
                        measure_dif = str(round(df[(df['drug'] == x) & (
                            (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['total_drug_forum'].values[0], 3))

                        stat = "There was is only one measurement over the {} period for {} ({}). {} comments & posts were flagged.\n".format(
                            period, drug_name, year, measure_dif)
                        summary_stat += stat + "\n"  # Add a new line here

                    else:
                        measure1 = round(df.loc[(df['drug'] == x) & (
                            df['year'] == sy[0]), 'total_drug_forum'].values[0], 3)
                        measure2 = round(df.loc[(df['drug'] == x) & (
                            df['year'] == sy[-1]), 'total_drug_forum'].values[0], 3)
                        measure_differ = "{} - {}".format(measure1, measure2)

                        period = "{}-{}".format(sy[0], sy[-1])
                        if measure1 < measure2:
                            direction = "an increase"
                        else:
                            direction = 'a decrease'

                        stat = "There was {} over the {} period for **{}**. **{}** comments & posts were flagged.\n".format(direction,
                                                                                                                   period,
                                                                                                                   drug_name,
                                                                                                                   measure_differ)
                        summary_stat += stat + "\n"  # Add a new line here

    return summary_stat


def reddit_text(df):
    sorted_countries = sorted(list(set(df['Country'].tolist())))
    number_countries = len(sorted_countries)

    number_year = len(set(df['year']))
    sorted_year = sorted(list(set(df['year'])))
    title = ''
    stat = ''

    if number_countries > 3:
        title_fin = "UNABLE TO GENERATE TEXT WHEN THERE IS MORE THAN THREE COUNTRIES SELECTED"
    else:
        if number_countries == 1:
            title = "The country that you have selected is **{}**. ".format(
                sorted_countries[0].capitalize())
            stat = reddit_text_gen(df, number_countries,
                                   sorted_countries, number_year, sorted_year)
        elif number_countries == 2:
            title = "The countries that you have selected are **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize())
            stat = reddit_text_gen(df, number_countries,
                                   sorted_countries, number_year, sorted_year)
        elif number_countries == 3:
            title = "The countries that you have selected are **{}**, **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize(), sorted_countries[2].capitalize())
            stat = reddit_text_gen(df, number_countries,
                                   sorted_countries, number_year, sorted_year)
        if number_year == 1:
            title2 = "The year of interest is **{}**. \n".format(sorted_year[0])
        else:
            title2 = "The selected period is **{} - {}**. \n".format(
                sorted_year[0], sorted_year[-1])
    title_fin = title + "\n" + title2 + "\n" + stat
    return title_fin

def reddit_text_gen(df, nc, sc, ny, sy):
    summary_stat = "Reddit Analysis:\n\n"
    measure = ''
    # single year
    if ny == 1:
        if nc == 1:
            for x in sorted(list(set(df['drug']))):
                measure = str(
                    round(df.loc[df['drug'] == x, 'total'].values[0], 3))
                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                stat = "**{}** Posts related to **{}**\n".format(
                    measure, drug_name)
                summary_stat += stat + "\n"
        else:
            for c in sc:
                summary_stat += "\n**Country: {}**\n".format(c.capitalize())
                for x in sorted(list(set(df['drug']))):
                    measure = str(
                        round(df.loc[df['drug'] == x, 'total'].values[0], 3))
                    drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                    stat = "**{}** comments & posts related to **{}**\n".format(
                        measure, drug_name)
                    summary_stat += stat + "\n"
    else:
        # more than one year
        if nc == 1:
            # only one country
            for x in sorted(list(set(df['drug']))):

                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                if len(df.loc[df['drug'] == x]) == 1:
                    period = "{}-{}".format(sy[0], sy[-1])
                    year = str(round(df[(df['drug'] == x) & (
                        (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['year'].values[0], 3))
                    measure_dif = str(round(df[(df['drug'] == x) & (
                        (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['total'].values[0], 3))
                    stat = "There was is only one measurement over the {} period for **{}** ({}). **{}** comments & posts were flagged.\n".format(
                        period, drug_name, year, measure_dif)
                    summary_stat += stat + "\n"

                else:

                    measure1 = round(df.loc[(df['drug'] == x) & (
                        df['year'] == sy[0]), 'total'].values[0], 3)
                    measure2 = round(df.loc[(df['drug'] == x) & (
                        df['year'] == sy[-1]), 'total'].values[0], 3)
                    measure_differ = "**{}** - **{}**".format(measure1, measure2)

                    period = "{}-{}".format(sy[0], sy[-1])
                    if measure1 < measure2:
                        direction = "an increase"
                    else:
                        direction = 'a decrease'

                    stat = "There was {} over the {} period for {}. **{}** comments & posts were seen.\n".format(direction,
                                                                                                                period,
                                                                                                                drug_name,
                                                                                                                measure_differ)
                    summary_stat += stat + "\n"
        else:
            # more than one country
            for c in sc:
                summary_stat += "\n**Country: {}**\n".format(c.capitalize())
                for x in sorted(list(set(df['drug']))):

                    drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                    if len(df.loc[df['drug'] == x]) == 1:
                        period = "{}-{}".format(sy[0], sy[-1])
                        year = str(round(df[(df['drug'] == x) & (
                            (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['year'].values[0], 3))
                        measure_dif = str(round(df[(df['drug'] == x) & (
                            (df['year'] == sy[0]) | (df['year'] == sy[-1]))]['total'].values[0], 3))
                        stat = "There was is only one measurement over the {} period for {} ({}). **{}** comments & posts were flagged.\n".format(
                            period, drug_name, year, measure_dif)
                        summary_stat += stat + "\n"

                    else:

                        measure1 = round(df.loc[(df['drug'] == x) & (
                            df['year'] == sy[0]), 'total'].values[0], 3)
                        measure2 = round(df.loc[(df['drug'] == x) & (
                            df['year'] == sy[-1]), 'total'].values[0], 3)
                        measure_differ = "**{}** - **{}**".format(measure1, measure2)

                        period = "{}-{}".format(sy[0], sy[-1])
                        if measure1 < measure2:
                            direction = "an increase"
                        else:
                            direction = 'a decrease'

                        stat = "There was {} over the {} period for {}.  **{}** comments & posts were flagged.\n".format(direction,
                                                                                                                        period,
                                                                                                                        drug_name,
                                                                                                                        measure_differ)
                        summary_stat += stat + "\n"

    return summary_stat

def un_drug_report_text(df):
    sorted_countries = sorted(list(set(df['Country'].tolist())))
    number_countries = len(sorted_countries)

    number_year = len(set(df['Year']))
    sorted_year = sorted(list(set(df['Year'])))
    title = ''
    stat = ''

    if len(set(df['Country'].tolist())) > 2:
        title_fin = "**UNABLE TO GENERATE TEXT WHEN THERE IS MORE THAN THREE COUNTRIES SELECTED**"
    else:
        if number_countries == 1:
            title = "The country that you have selected is **{}**. ".format(
                sorted_countries[0].capitalize())
            stat = un_drug_text(df, number_countries,
                                sorted_countries, number_year, sorted_year)
        elif number_countries == 2:
            title = "The countries that you have selected are **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize())
            stat = un_drug_text(df, number_countries,
                                sorted_countries, number_year, sorted_year)
        elif number_countries == 3:
            title = "The countries that you have selected are **{}**, **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize(), sorted_countries[2].capitalize())
            stat = un_drug_text(df, number_countries,
                                sorted_countries, number_year, sorted_year)
        if number_year == 1:
            title2 = "The year of interest is **{}**. \n".format(sorted_year[0])
        else:
            title2 = "The selected period is **{} - {}**. \n".format(
                sorted_year[0], sorted_year[-1])
    title_fin = title + "\n" + title2 + "\n" + stat
    return title_fin


def un_drug_text(df, nc, sc, ny, sy):
    summary_stat = "UN World Drug Report Analysis:\n\n"
    measure = ''

    for c in sc:
        #summary_stat += "\n**Country: {}**\n".format(c.capitalize())
        for x in sorted(list(set(df['Metabolite']))):
            drug_name = str(
                df.loc[df['Metabolite'] == x, 'Metabolite'].values[0])

            if ny == 1:
                subset = df.loc[(df['Metabolite'] == x) & (df['Country'] == c), 'Percentage of the population']
                measure = round(subset.values[0], 3) if not subset.empty else 0.0
                stat = "**{}** per litre/day per 1 000 inhabitants for **{}**\n".format(
                    measure, drug_name)
                summary_stat += stat + "\n"
            else:
                subset = df.loc[(df['Metabolite'] == x) & (df['Country'] == c) & (df['Year'] == sy[0]), 'Percentage of the population']
                measure1 = round(subset.values[0], 3) if not subset.empty else 0.0
                subset = df.loc[(df['Metabolite'] == x) & (df['Country'] == c) & (df['Year'] == sy[-1]), 'Percentage of the population']
                measure2 = round(subset.values[0], 3) if not subset.empty else 0.0

                period = "{}-{}".format(sy[0], sy[-1])
                measure_differ = "**{}** - **{}**".format(measure1, measure2)

                if measure1 < measure2:
                    direction = "an increase"
                else:
                    direction = 'a decrease'

                stat = "There was {} over the {} period for **{}**. **{}** - **{}** (per litre/day per 1 000 inhabitants).\n".format(
                    direction, period, drug_name, measure1, measure2)
                summary_stat += stat + "\n"

    return summary_stat


def waste_water_text(df):
    sorted_countries = sorted(list(set(df['Country'].tolist())))
    number_countries = len(sorted_countries)

    # return print(sorted_countries)
    number_year = len(set(df['Year']))
    sorted_year = sorted(list(set(df['Year'])))
    title = ''
    stat = ''

    if len(set(df['Country'].tolist())) > 2:
        returned_text = "**UNABLE TO GENERATE TEXT WHEN THERE IS MORE THAN THREE COUNTRIES SELECTED**"
    else:
        if number_countries == 1:
            title = "The country that you have selected is **{}**. ".format(
                sorted_countries[0].capitalize())
            stat = waste_water_drug_text(
                df, number_countries, sorted_countries, number_year, sorted_year)
        elif number_countries == 2:
            title = "The countries that you have selected are **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize())
            stat = waste_water_drug_text(
                df, number_countries, sorted_countries, number_year, sorted_year)
        elif number_countries == 3:
            title = "The countries that you have selected are **{}**, **{}** & **{}**. ".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize(), sorted_countries[2].capitalize())
            stat = waste_water_drug_text(
                df, number_countries, sorted_countries, number_year, sorted_year)
        if number_year == 1:
            title2 = "The year of interest is **{}**. \n".format(sorted_year[0])
        else:
            title2 = "The selected period is **{} - {}**. \n".format(
                sorted_year[0], sorted_year[-1])
        title_fin = title + "\n" + title2 + "\n" + stat

        returned_text = title_fin

    return returned_text


def waste_water_drug_text(df, nc, sc, ny, sy):
    summary_stat = "European Wastewater Analysis:\n\n"
    
    if ny == 1:
        if nc == 1:
            for x in sorted(list(set(df['Metabolite']))):
                subset_df = df.loc[df['Metabolite'] == x, 'litre/day per 1 000 inhabitants']
                if not subset_df.empty:
                    measure = str(round(subset_df.values[0], 4))
                    drug_name = str(df.loc[df['Metabolite'] == x, 'Metabolite'].values[0])

                    stat = "**{}** per litre/day per 1 000 inhabitants for **{}**\n".format(measure, drug_name)
                    summary_stat += stat + "\n"
        else:
            for c in sc:
                summary_stat += "\n**Country: {}**\n".format(c.capitalize())
                for x in sorted(list(set(df['Metabolite']))):
                    subset_df = df.loc[(df['Metabolite'] == x) & (df['Country'] == c), 'litre/day per 1 000 inhabitants']
                    if not subset_df.empty:
                        measure = str(round(subset_df.values[0], 4))
                        drug_name = str(df.loc[df['Metabolite'] == x, 'Metabolite'].values[0])

                        stat = "**{}** per litre/day per 1 000 inhabitants for **{}**\n".format(measure, drug_name)
                        summary_stat += stat + "\n"
    else:
        if nc == 1:
            for x in sorted(list(set(df['Metabolite']))):
                subset_df1 = df.loc[(df['Metabolite'] == x) & (df['Year'] == sy[0]), 'litre/day per 1 000 inhabitants']
                subset_df2 = df.loc[(df['Metabolite'] == x) & (df['Year'] == sy[-1]), 'litre/day per 1 000 inhabitants']
                
                if not subset_df1.empty and not subset_df2.empty:
                    measure1 = round(subset_df1.values[0], 4)
                    measure2 = round(subset_df2.values[0], 4)

                    period = "{}-{}".format(sy[0], sy[-1])
                    if measure1 < measure2:
                        direction = "an increase"
                    else:
                        direction = 'a decrease'

                    drug_name = str(df.loc[df['Metabolite'] == x, 'Metabolite'].values[0])

                    stat = "There was {} over the {} period for **{}**. **{}** - **{}** (per litre/day per 1 000 inhabitants).\n".format(direction,
                                                                                                                                     period,
                                                                                                                                     drug_name,
                                                                                                                                     measure1, measure2)
                    summary_stat += stat + "\n"
        else:
            for c in sc:
                summary_stat += "\n**Country: {}**\n".format(c.capitalize())
                for x in sorted(list(set(df['Metabolite']))):
                    subset_df1 = df.loc[(df['Metabolite'] == x) & (df['Year'] == sy[0]) & (df['Country'] == c), 'litre/day per 1 000 inhabitants']
                    subset_df2 = df.loc[(df['Metabolite'] == x) & (df['Year'] == sy[-1]) & (df['Country'] == c), 'litre/day per 1 000 inhabitants']

                    if not subset_df1.empty and not subset_df2.empty:
                        measure1 = round(subset_df1.values[0], 4)
                        measure2 = round(subset_df2.values[0], 4)

                        period = "{}-{}".format(sy[0], sy[-1])
                        if measure1 < measure2:
                            direction = "an overall increase"
                        else:
                            direction = 'an overall decrease'

                        drug_name = str(df.loc[df['Metabolite'] == x, 'Metabolite'].values[0])

                        stat = "There was {} over the {} period for **{}**. **{}** - **{}** (per litre/day per 1 000 inhabitants).\n".format(direction,
                                                                                                                                     period,
                                                                                                                                     drug_name,
                                                                                                                                     measure1, measure2)
                        summary_stat += stat + "\n"

    return summary_stat


def drug_lab(df):
    sorted_countries = sorted(list(set(df['Country'].tolist())))
    number_countries = len(sorted_countries)

    title = ''
    stat = ''

    if number_countries > 3:
        title_fin = "**UNABLE TO GENERATE TEXT WHEN THERE IS MORE THAN THREE COUNTRIES SELECTED**"
    else:
        if number_countries == 1:
            title = "The country that you have selected is **{}**. \n\n".format(
                sorted_countries[0].capitalize())
            stat = drug_lab_gen(df, number_countries, sorted_countries)
        elif number_countries == 2:
            title = "The countries that you have selected are **{}** & **{}**. \n\n".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize())
            stat = drug_lab_gen(df, number_countries, sorted_countries)
        elif number_countries == 3:
            title = "The countries that you have selected are **{}**, **{}** & **{}**. \n\n".format(
                sorted_countries[0].capitalize(), sorted_countries[1].capitalize(), sorted_countries[2].capitalize())
            stat = drug_lab_gen(df, number_countries, sorted_countries)

    title_fin = title + stat
    return title_fin

def drug_lab_gen(df, nc, sc):
    summary_stat = "European Drug Report Analysis:\n\n"
    measure = ''

    if nc == 1:
        for c in sc:
            # No need to add the "Country: {}" line
            for x in sorted(list(set(df['drug']))):
                measure = str(
                    round(df.loc[df['drug'] == x, 'percentage_of_post'].values[0], 3))
                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                stat = "Percentage of {} entrants into treatment was **{}%**\n".format(
                    drug_name, measure)
                summary_stat += stat + "\n"
    else:
        for c in sc:
            summary_stat += "\n**Country: {}**: ".format(c.capitalize())
            for x in sorted(list(set(df['drug']))):
                drug_name = str(df.loc[df['drug'] == x, 'drug'].values[0])

                if len(df.loc[df['drug'] == x]) == 1:
                    measure_dif = str(
                        round(df.loc[df['drug'] == x, 'percentage_of_post'].values[0], 3))
                    stat = " There was is only one measurement for **{}** (**{}%**). **{}** comments & posts were flagged. \n ".format(
                        drug_name, measure_dif)
                    summary_stat += stat + "\n"
                else:
                    measure_differ = round(
                        df.loc[df['drug'] == x, 'percentage_of_post'], 3)
                    stat = " Comments & posts were flagged for **{}**. \n ".format(
                        drug_name, measure_differ)
                    summary_stat += stat + "\n"

    return summary_stat
