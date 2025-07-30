import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D  # type: ignore
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl
# Use Arial font
mpl.rc('font', family='Arial')

# Section 1: HVI by Neighborhood (Bubble Chart)
sns.set_style('whitegrid')
# prepare data for bubble chart with correct HVI assignments
data = {
    'Neighborhood':['Morrisania/East Tremont','Brownsville','Hunts Point/Mott Haven','Chelsea','Upper East Side','Brooklyn Heights'],
    'HVI':[5,5,4,3,2,1],
    'MedianIncome':[25,30,24,60,101,85],  # in thousands
    'PctWithoutAC':[24.2,20.1,15.7,12.0,3.1,5.2],
    'PctBlackLatino':[60,75,55,25,10,15]  # approximate values for demo
}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(10,7))
# Set figure and axes background colors
fig.patch.set_facecolor('#F5F2E8')
ax.set_facecolor('white')
# Disable axes background patch
ax.patch.set_visible(False)

# bubble chart: equal-sized bubbles
sizes = [200] * len(df)
# Updated color palette - dark blue for HVI 2, maroon for HVI 5
color_map = {5:'#800000',4:'#663399',3:'#006400',2:'#003366',1:'#FFFFFF'}
colors = [color_map[h] for h in df['HVI']]
# Add black edge to HVI 5 bubbles
edgecolors = ['black' if h == 5 else 'k' for h in df['HVI']]
linewidths = [1.5 if h == 5 else 1 for h in df['HVI']]

# Create scatter plot without events/trigger data - just showing HVI distribution
x_positions = [89, 90, 91.5, 93, 97, 95]  # distribute horizontally for visibility
y_positions = [6, 5, 3, 2, 1, 0.5]  # distribute vertically for visibility

sc = plt.scatter(x_positions, y_positions, s=sizes, c=colors,
                alpha=0.6, edgecolor=edgecolors, linewidth=linewidths, zorder=3)
# axis formatting - loop through spines for consistent styling
for spine in ax.spines.values():
    spine.set_linewidth(1.5)
    spine.set_edgecolor('black')
    spine.set_visible(True)

ax.tick_params(axis='both', which='major', labelsize=12)
# make tick labels and rotate x-axis labels 45° with 12pt font and padding
for lbl in ax.get_xticklabels():
    lbl.set_fontweight('normal')
    lbl.set_rotation(45)
    lbl.set_fontsize(12)
    lbl.set_fontfamily('Arial')
for lbl in ax.get_yticklabels():
    lbl.set_fontweight('bold')
    lbl.set_fontfamily('Arial')
ax.tick_params(axis='x', pad=10)
ax.xaxis.grid(False)
ax.yaxis.grid(True, linewidth=1, alpha=0.3)

# Set equal scaling and explicit limits
ax.set_aspect('auto')
ax.set_xlim(88,98)
ax.set_ylim(0,8)

# Updated titles
fig.suptitle('NYC Heat Vulnerability Index by Neighborhood', fontsize=16, fontweight='bold', fontfamily='Arial')
ax.set_title('Social Vulnerability Distribution Across NYC Districts', fontsize=12,
             fontstyle='italic', pad=10, fontfamily='Arial')
ax.set_xlabel('Geographic Distribution', fontsize=12, fontfamily='Arial')
ax.set_ylabel('Vulnerability Level', fontsize=12, fontfamily='Arial')

# Add HVI labels directly over each bubble
for i, row in df.iterrows():
    hvi_label = f"HVI {row['HVI']}"
    ax.annotate(hvi_label, xy=(x_positions[i], y_positions[i]),
                xytext=(0, 15), textcoords='offset points',
                fontsize=9, fontfamily='Arial', ha='center', fontweight='bold')
# No legend needed since HVI labels are directly on bubbles

# Adjust spacing with increased top margin for title and more bottom space for table
fig.subplots_adjust(top=0.88, bottom=0.20)

# Create proper DataFrame table with HVI column
table_data = df[['Neighborhood','PctWithoutAC','PctBlackLatino','MedianIncome','HVI']].round(1)
table_data.columns = ['Neighborhood','% Without AC','% Black/Latino','Median Income (k)','HVI']

# Position table as inset below the chart
table_ax = fig.add_axes([0.1, 0.05, 0.8, 0.15])
table_ax.axis('off')
# Style the table background
table_ax.patch.set_facecolor('#F5F2E8')
table_ax.patch.set_edgecolor('black')
table_ax.patch.set_linewidth(1)

# Create table with matplotlib - proper DataFrame structure
table_vals = table_data.values
col_labels = ['Neighborhood','% Without AC','% Black/Latino','Median Income (k)','HVI']
table = table_ax.table(cellText=table_vals, colLabels=col_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1,1.2)
for key, cell in table.get_celld().items():
    cell.set_linewidth(0)
    cell.set_facecolor('white')
    cell.set_text_props(fontfamily='Arial', fontsize=10)

# Add HVI mapping text box above table
hvi_mapping = 'HVI 5 = Morrisania/East Tremont, Brownsville; HVI 4 = Hunts Point/Mott Haven; HVI 3 = Chelsea; HVI 2 = Upper East Side; HVI 1 = Brooklyn Heights'
ax.text(0.5, -0.35, hvi_mapping, transform=ax.transAxes, fontsize=9, 
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'), 
        ha='center', va='top', fontfamily='Arial')

plt.tight_layout(pad=1.1, rect=[0,0.18,1,1])
plt.savefig('hvi_by_neighborhood.png', bbox_inches='tight')
plt.close()
print('[Saved: hvi_by_neighborhood.png]')

# Section 2: Health Impact of Extreme Heat (2010–22)
data2 = {
    'Metric':['Asthma Rate (%)','% Over 65','ER Visits (per 10k)','Heat Deaths (per mil)'],
    'Morrisania/East Tremont':[12.2,15,18.5,0.8],
    'Upper East Side':[4.1,21,6.4,0.4]
}
df2 = pd.DataFrame(data2).set_index('Metric')
fig, ax = plt.subplots(figsize=(12,6))
df2.plot(kind='bar', color=['#003366','#606060'], ax=ax)
ax.set_title('Health Impact of Extreme Heat (2010–22): ER Visits, Asthma & Heat Deaths by Neighborhood', fontsize=14, pad=50)
ax.set_ylabel('Rate per 10 k / % / Deaths per M', fontsize=12)
ax.set_xticklabels(df2.index, rotation=0, fontsize=10)
ax.set_xlabel(ax.get_xlabel(), labelpad=30)
ax.legend(title='Neighborhood', loc='upper left', bbox_to_anchor=(1.02,0.8), frameon=False)
# footnote
fig.text(0.5, -0.1, 'Sources: NYC DOHMH Community Health Profiles (2018–2022) for ER visits & asthma; NYC DOH Heat Mortality Reports (2010–2020 avg.) for heat deaths; U.S. Census ACS (2019–2021) for age breakdown.', fontsize=9, style='italic', color='gray', ha='center')
plt.tight_layout(pad=1.2)
fig.subplots_adjust(top=0.75, bottom=0.2, left=0.1, right=0.8)
fig.savefig('health_burden_comparison.png', bbox_inches='tight')
plt.close()
print('[Saved: health_burden_comparison.png]')

# Section 3: Trigger Threshold vs Payout Events
data3 = {
    'Neighborhood':['Morrisania','Hunts Point','Upper East Side'],
    'TriggerHI':[89,91.5,97],
    'Events':[7,3,1],
    'HVI':[5,5,2],
    'PctWithoutAC':[24.2,15.7,3.1],
    'MedianIncome':['$25k','$24k','$101k']
}
df3 = pd.DataFrame(data3)
fig = plt.figure(figsize=(10,6))
# Expanded to include spacer row
gs = fig.add_gridspec(nrows=6, ncols=1, height_ratios=[0.6,4,0.3,0.3,1,0.7], hspace=0.5)

### Title Row
ax_title = fig.add_subplot(gs[0,0])
ax_title.axis('off')
ax_title.text(0.5,0.5,'3-day HI Trigger vs Payout Events by Neighborhood',fontsize=18,fontweight='bold',ha='center',va='center')

### Main Bubble Chart Row
ax = fig.add_subplot(gs[1,0])
palette = {5:'#800000',2:'#000080'}
# equal-sized dots
sizes = [150] * len(df3)
ax.scatter(df3['TriggerHI'], df3['Events'], s=sizes, c=df3['HVI'].map(palette), edgecolor='k', alpha=0.95)
ax.axvspan(88,95,color='#FFCCCC',alpha=0.3)
ax.axvline(95,color='grey',linestyle='--',linewidth=2)
for _,row in df3.iterrows(): ax.text(row.TriggerHI+0.5,row.Events,row.Neighborhood,fontsize=10,va='center')
ax.set_xlim(87,99); ax.set_ylim(0,8)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_xlabel('Trigger Heat Index (°F)',labelpad=10)
ax.set_ylabel('Events (2018-2022)',labelpad=10)
 # move x-axis label and elements below down
ax.xaxis.set_label_coords(0.5,-0.15)
legend_elements = [Line2D([0],[0],marker='o',color='w',label=f'HVI {k}',markerfacecolor=v,markersize=10) for k,v in palette.items()]
ax.legend(handles=legend_elements,title='HVI',loc='upper right')

### Spacer Row (blank for extra spacing)
blank_ax = fig.add_subplot(gs[2,0]); blank_ax.axis('off')

### Subtitle Row
ax_sub = fig.add_subplot(gs[3,0]); ax_sub.axis('off')
ax_sub.text(0.5,0.5,'Lower trigger thresholds concentrate payouts in vulnerable neighborhoods',fontsize=13,style='italic',ha='center',va='center')

### Table Row
ax_table = fig.add_subplot(gs[4,0]); ax_table.axis('off')
# Prepare table data with correct DataFrame columns
table_data = df3[['Neighborhood','PctWithoutAC','MedianIncome']].values
col_labels = ['Neighborhood','% Without AC','Median Income']
tbl = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1,1.2)
for (i,j),cell in tbl.get_celld().items():
    cell.set_edgecolor('black'); cell.set_linewidth(1)
    if i==0:
        cell.set_text_props(weight='bold'); cell.set_facecolor('#E6E6E6')

### Caption Row
ax_cap = fig.add_subplot(gs[5,0]); ax_cap.axis('off')
ax_cap.text(0.5,0.5,'Lower trigger thresholds and more payouts concentrate in vulnerable neighborhoods, proving policy fairness.',ha='center',va='center',fontsize=10)

plt.tight_layout(); plt.savefig('trigger_vs_events.png',bbox_inches='tight'); plt.close()
print('[Saved: trigger_vs_events.png]')

# Section 4: Social and Demographic Vulnerability Comparison
import matplotlib as mpl
mpl.rc('font', family='Liberation Sans')
metrics = ['% Without AC', '% Black/Latino', '% Under Poverty', '% Seniors', 'SVI Score']
values_bro = [18.3, 80, 38, 13, 0.85]
values_ues = [3.1, 10, 7, 21, 0.18]
bar_width = 0.35
indices = list(range(len(metrics)))
fig, ax = plt.subplots(figsize=(8,5))
fig.subplots_adjust(top=0.90)
# plot bars with special color for % Without AC
colors_bro = ['#003366'] * len(metrics)
colors_ues = ['#7F7F7F'] * len(metrics)
ax.bar(indices, values_bro, width=bar_width, color=colors_bro, label='Brownsville')
ax.bar([i+bar_width for i in indices], values_ues, width=bar_width, color=colors_ues, label='Upper East Side')
# gridlines
ax.grid(axis='y', linestyle='--', color='lightgray', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# labels
ax.set_xticks([i+bar_width/2 for i in indices])
ax.set_xticklabels(metrics, rotation=45, fontsize=10)
ax.set_ylabel('Percent / Index', fontsize=12)
# title and subtitle
fig.suptitle('Heat Vulnerability Drivers: Brownsville vs. UES', fontsize=16, fontweight='bold')
ax.set_title('High social vulnerability & low AC access → elevated heat illness risk', fontsize=12, fontstyle='italic', pad=10)
# horizontal threshold line
ax.axhline(20, color='red', linestyle='--', linewidth=1)
ax.text(len(metrics)-0.1, 21, 'Critical AC access threshold', color='red', fontsize=10, va='bottom', ha='right')
# annotate disparity on % Black/Latino
i = metrics.index('% Black/Latino')
ax.annotate('8× higher vulnerability', xy=(i, values_bro[1]), xytext=(i, values_bro[1]+5),
              arrowprops=dict(arrowstyle='->', color='black'), fontsize=9)
# inset text box
ax.text(0.6, 0.7, 'Projected 15% reduction in ER visits', transform=ax.transAxes,
        fontsize=9, bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'), ha='left', va='top')
# legend outside
ax.legend(loc='upper left', bbox_to_anchor=(1,1), frameon=False)
# adjust limits
left_lim = -bar_width*0.1
right_lim = len(metrics) - 1 + bar_width*1.1
ax.set_xlim(left_lim, right_lim)
# footnote
fig.text(0.01, 0.01,
         'Parametric trigger: AC-lack >20% & 2-day heat-index ≥ 95 °F',
         fontsize=9, fontstyle='italic', color='gray')
plt.tight_layout(pad=1.2)
plt.savefig('demographic_comparison.png', bbox_inches='tight')
plt.close()
print('[Saved: demographic_comparison.png]')

# End of Section 4
print('DONE.')
