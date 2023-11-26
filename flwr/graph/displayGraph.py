import matplotlib.pyplot as plt
from datetime import datetime
import os

curr_time = datetime.now().strftime("%d%m%Y-%H%M%S")
output_dir = "/home/emok/sq58/Code/base_mammo/flwr/performance_metrics"
output_metric_file = os.path.join(output_dir, f"{curr_time}_metric.jpeg")
output_loss_file = os.path.join(output_dir, f"{curr_time}_loss.jpeg")

# Copy data from log files
# TODO Make it create the graph automatically after finishing the FL rounds
# Data for the metrics
metrics = {
    'recall': [(1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 0.9655765996311622), (6, 0.9960090082385473), (7, 0.8224942534387503), (8, 0.7675235203527906), (9, 0.6895708465763327), (10, 0.8576024838354297), (11, 0.7003660656195719), (12, 0.5607909225459079), (13, 0.5075783227050858), (14, 0.4978060340891324), (15, 0.5414726590174366), (16, 0.5331404025981711), (17, 0.47444747969591605), (18, 0.36647895144090126), (19, 0.39535661409233647), (20, 0.29414953008069117)], 'auc': [(1, 0.5), (2, 0.5), (3, 0.5), (4, 0.5), (5, 0.531127542886715), (6, 0.5015963967045811), (7, 0.5321980665683003), (8, 0.547361652207759), (9, 0.5226120914760807), (10, 0.5708817780279282), (11, 0.6134099339445984), (12, 0.5748646694798891), (13, 0.617665479266374), (14, 0.6169178607542505), (15, 0.5891750315213907), (16, 0.6051584199028467), (17, 0.6048273986022612), (18, 0.5808870275202549), (19, 0.5993695550566069), (20, 0.5717744370464406)], 'precision': [(1, 0.5759879396576812), (2, 0.5759879396576811), (3, 0.5759879396576811), (4, 0.5759879396576811), (5, 0.5956546788305835), (6, 0.5768110817084809), (7, 0.6235699742649646), (8, 0.6258422413313511), (9, 0.6360095854190138), (10, 0.6225437176557803), (11, 0.6705168079646529), (12, 0.6809239832494953), (13, 0.7233643748362583), (14, 0.7701965386291247), (15, 0.6900582254832265), (16, 0.7326177130152491), (17, 0.7121789024639439), (18, 0.7260417638939702), (19, 0.7293794509533488), (20, 0.7471256170077424)], 'loss': [(1, 0.8326247170189026), (2, 0.8036804334913238), (3, 1.0972912006521718), (4, 0.9191233931233719), (5, 0.846795523155442), (6, 0.791148663856797), (7, 0.7718046017671013), (8, 0.6182136301823865), (9, 0.5687738036279508), (10, 0.6173866675467504), (11, 0.608922207456429), (12, 0.5513824355120044), (13, 0.6555760947467018), (14, 0.557702537874848), (15, 0.5400310397596709), (16, 0.6080287093838094), (17, 0.5285562550472069), (18, 0.4972157761216276), (19, 0.5630001832826566), (20, 0.7223449571028365)], 'accuracy': [(1, 0.5759879396576812), (2, 0.5759879396576811), (3, 0.5759879396576811), (4, 0.5759879396576811), (5, 0.6071154825443962), (6, 0.5775843363622623), (7, 0.6207307821749101), (8, 0.4959679869075025), (9, 0.4400660092810042), (10, 0.5558509306994998), (11, 0.6157503360986105), (12, 0.4893638437125378), (13, 0.6419089220970012), (14, 0.5958691960048919), (15, 0.527788685698294), (16, 0.6399667882592549), (17, 0.5768375385804679), (18, 0.5047681305777368), (19, 0.5768639333817295), (20, 0.5095917384861395)], 'prauc': [(1, 0.7879939698288406), (2, 0.7879939698288406), (3, 0.7879939698288406), (4, 0.7879939698288406), (5, 0.7892214893230824), (6, 0.7874077929138773), (7, 0.7645718256017794), (8, 0.7817157301686593), (9, 0.7773400624798478), (10, 0.791390389512727), (11, 0.7729082667880611), (12, 0.7685660059017736), (13, 0.7452257527032874), (14, 0.7784775866266943), (15, 0.7606445948600822), (16, 0.7554029910257373), (17, 0.7465824878694999), (18, 0.7413727707297598), (19, 0.733427555044563), (20, 0.7291016086687485)], 'f1_score': [(1, 0.7223009761803006), (2, 0.7223009761803006), (3, 0.7223009761803006), (4, 0.7223009761803006), (5, 0.729484967178237), (6, 0.7221199415024616), (7, 0.6780005115805563), (8, 0.6094990234914591), (9, 0.5135151744910103), (10, 0.6821204660488952), (11, 0.6677909838849324), (12, 0.49818756195736164), (13, 0.5798131345440499), (14, 0.5634656587877592), (15, 0.5453305569170346), (16, 0.5951678642246477), (17, 0.5412588386602012), (18, 0.4257718516254061), (19, 0.49800763048477414), (20, 0.378728817782692)]
}

# Create subplots for each metric
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 8))
NUM_ROUNDS = len(metrics['loss'])
x_intervals = [x for x in range(1, NUM_ROUNDS+1, 2)]

# Plot accuracy
axes[0, 0].plot(*zip(*metrics['accuracy']))
axes[0, 0].set_title('Accuracy')
axes[0, 0].set_xlabel('FL Round')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_xticks(x_intervals)
axes[0, 0].set_ylim(0, 1)

# Plot precision
axes[0, 1].plot(*zip(*metrics['precision']))
axes[0, 1].set_title('Precision')
axes[0, 1].set_xlabel('FL Round')
axes[0, 1].set_ylabel('Precision')
axes[0, 1].set_xticks(x_intervals)
axes[0, 1].set_ylim(0, 1)


# Plot recall
axes[1, 0].plot(*zip(*metrics['recall']))
axes[1, 0].set_title('Recall')
axes[1, 0].set_xlabel('FL Round')
axes[1, 0].set_ylabel('Recall')
axes[1, 0].set_xticks(x_intervals)
axes[1, 0].set_ylim(0, 1)

# Plot F1-score
axes[1, 1].plot(*zip(*metrics['f1_score']))
axes[1, 1].set_title('F1 Score')
axes[1, 1].set_xlabel('FL Round')
axes[1, 1].set_ylabel('Loss')
axes[1, 1].set_xticks(x_intervals)
axes[1, 1].set_ylim(0, 1)

# Plot AUC
axes[2, 0].plot(*zip(*metrics['auc']))
axes[2, 0].set_title('AUC')
axes[2, 0].set_xlabel('FL Round')
axes[2, 0].set_ylabel('AUC')
axes[2, 0].set_xticks(x_intervals)
axes[2, 0].set_ylim(0, 1)

# Plot PRAUC
axes[2, 1].plot(*zip(*metrics['prauc']))
axes[2, 1].set_title('PRAUC')
axes[2, 1].set_xlabel('FL Round')
axes[2, 1].set_ylabel('PRAUC')
axes[2, 1].set_xticks(x_intervals)
axes[2, 1].set_ylim(0, 1)

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig(output_metric_file)

# Plot losses
plt.clf()
plt.figure(figsize=(8, 4))
plt.plot(*zip(*metrics['loss']))
plt.xticks(x_intervals)
plt.title('Loss')
plt.xlabel('FL Round')
plt.ylabel('Loss')
plt.grid(True)
plt.savefig(output_loss_file)
