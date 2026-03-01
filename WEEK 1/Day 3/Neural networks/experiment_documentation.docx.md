

**Lab M1.04**

**Build Simple Neural Network**

*Experiment Documentation & Findings*

Dataset: CIFAR-10 (Dogs vs Cats)

March 2026

# **Overview**

This document records all hyperparameter experiments conducted during Lab M1.04. Each experiment tests one variable while holding all others constant (baseline), allowing direct comparison of results. All experiments use the CIFAR-10 dog/cat subset (\~10,000 training images, 2,000 test images).

| Parameter | Baseline Value |
| :---- | :---- |
| Architecture | Dense(128, relu) \-\> Dense(64, relu) \-\> Dense(1, sigmoid) |
| Optimizer | Adam (lr=0.001) |
| Loss | Binary Crossentropy |
| Batch Size | 32 |
| Epochs | 20 |
| Input | Flattened 32x32x3 \= 3072 features |
| Baseline Accuracy | \~60% |

# **Experiment 1: Number of Hidden Layers**

Question: Does adding more layers improve accuracy? Does depth help the model learn better features?

**Configurations Tested**

| Configuration | Val Accuracy | Overfit Gap | Train Time |
| :---- | :---- | :---- | :---- |
| 1 layer (128) | 50.0% | small | 40.2s |
| 2 layers (128-\>64) | 57.5% | small | 40.1s |
| 3 layers (128-\>64-\>32) | 58.1% | medium | 38.5s |
| **4 layers (128-\>64-\>32-\>16)** | **59.6%** | **medium** | **\~38s** |

**Key Findings**

More layers produced better accuracy, with 4 layers achieving the best result at 59.6%. However the gains showed clear diminishing returns: the jump from 1 to 2 layers was \+7.5%, while 3 to 4 layers gained only \+1.5%. Training time barely changed across all configurations since the later layers (32, 16 neurons) are very small.

Important caveat: the validation accuracy curves were noisy and bouncing throughout training rather than smoothly improving. This suggests the model may be memorizing rather than truly learning, since flattening the image destroys spatial relationships between pixels. A CNN architecture would be more appropriate for image classification.

**Conclusion**

Best config: 4 layers. However, adding more layers beyond 4 would likely not help without also addressing the fundamental limitation of using flattened input for image data.

# **Experiment 2: Number of Neurons per Layer**

Question: Does a wider network perform better? How does width relate to overfitting?

**Configurations Tested**

| Neurons | Val Accuracy | Overfit Gap | Notes |
| :---- | :---- | :---- | :---- |
| 32 | 60.7% | 1.4% | Low capacity |
| 64 | 59.4% | 3.5% | Moderate |
| 128 (baseline) | 50.9% | \-0.7% | Anomaly \- bad init |
| 256 | 60.3% | 3.5% | Good balance |
| **512** | **60.2%** | **4.6%** | **Most overfitting** |

**Key Findings**

Width had surprisingly little impact on validation accuracy \- all working configurations landed around 60%. The 128-neuron run was an anomaly (likely bad random initialization) producing a negative gap, meaning validation outperformed training, which is statistically unusual.

The most important observation is in the overfitting gap column: larger networks show bigger gaps (512 neurons \= 4.6% gap), confirming that more parameters create more capacity for memorization. The real bottleneck is the flattened input, not the network width.

**Conclusion**

No clear winner from width alone. The consistent \~60% ceiling across all configs confirms the fundamental problem is the flattened input losing spatial information, not insufficient network capacity.

# **Experiment 3: Learning Rate**

Question: How does the learning rate affect convergence speed and final accuracy?

**Configurations Tested**

| Learning Rate | Val Accuracy | Loss Curve | Behaviour |
| :---- | :---- | :---- | :---- |
| **0.0001 (very slow)** | **62.7%** | **Smooth, slow** | **Best final accuracy** |
| 0.001 (default) | 58.0% | Smooth, fast | Converges quickly |
| 0.01 (fast) | 60.4% | Bumpy | Overshooting |
| 0.1 (very fast) | 50.0% | Chaotic spike | Completely broken |

**Key Findings**

LR=0.1 completely failed, stuck at 50% (random guessing) for all 20 epochs. The loss chart showed it starting at 8.0 then crashing instantly \- the model took such a large step it got permanently stuck. LR=0.0001 surprisingly won at 62.7%, not because it is inherently better but because tiny steps allowed it to find a more precise position in 20 epochs while 0.001 kept bouncing around the optimal point.

However this result is epoch-dependent: with more epochs (100+), LR=0.001 would likely overtake 0.0001 since it converges faster. At 5 epochs specifically, LR=0.001 is the winner since it reaches a good position fastest.

**Conclusion**

Best config for 20 epochs: LR=0.0001. Best config for quick training (5 epochs): LR=0.001. LR=0.1 should never be used with Adam optimizer on this type of problem.

# **Experiment 4: Batch Size**

Question: How does batch size affect accuracy, stability, and training speed?

**Configurations Tested**

| Batch Size | Val Accuracy | Train Time | Loss Curve | Verdict |
| :---- | :---- | :---- | :---- | :---- |
| 16 (very small) | 60.7% | 74.7s | Stable | Best accuracy |
| **32 (default)** | **60.6%** | **49.0s** | **Stable** | **Sweet spot** |
| 64 (medium) | 56.7% | 24.7s | Smooth | Accuracy drop |
| 128 (large) | 55.1% | 16.9s | Very smooth | Fastest, worst |

**Key Findings**

A clear accuracy cliff exists between batch 32 and batch 64: accuracy drops from \~60.6% to 56.7%. Smaller batches update weights more frequently per epoch (batch 16 \= 625 updates vs batch 128 \= 78 updates), leading to better generalization.

Paradoxically, the loss charts showed larger batches achieving lower training loss despite worse validation accuracy \- a clear overfitting signal. Batch 128 is 4.4x faster than batch 16 but pays with 5.6% less accuracy. Batch 32 delivers 99.8% of batch 16 accuracy in 65% of the time, making it the optimal efficiency choice.

**Efficiency Comparison**

| Batch | Accuracy | Time | Accuracy per Second |
| :---- | :---- | :---- | :---- |
| 16 | 60.7% | 74.7s | 0.81%/s |
| **32** | **60.6%** | **49.0s** | **1.24%/s** |
| 64 | 56.7% | 24.7s | 2.29%/s |
| 128 | 55.1% | 16.9s | 3.26%/s |

**Conclusion**

Best config: Batch 32 (default). This explains why 32 is the industry-standard default \- it optimally balances accuracy and training speed.

# **Experiment 5: Number of Epochs**

Question: When does the model stop learning? When does overfitting begin?

**Configurations Tested**

| Epochs | Val Accuracy | Overfit Gap | Status |
| :---- | :---- | :---- | :---- |
| 5 | 56.2% | 3.7% | Underfitting \- not enough learning |
| 10 | 59.5% | 1.9% | Still improving |
| **20** | **60.0%** | **2.0%** | **Sweet spot \- best accuracy** |
| 50 | 58.7% | 6.6% | Overfitting \- accuracy drops |

**Key Findings**

The results demonstrate the classic underfitting-overfitting curve. The sweet spot for final accuracy is 20 epochs (60.0%), but the loss chart reveals the true learning stops around epoch 8-10. After this point, training loss keeps falling while validation loss flattens, meaning the model memorizes rather than learns.

Most tellingly, 50 epochs performed worse than 20 epochs (58.7% vs 60.0%) despite three times more training. The overfitting gap nearly tripled from 2.0% to 6.6%, proving that extra training actively hurt generalization performance.

**The Loss Chart Insight**

Accuracy alone is a misleading metric for this decision. The loss chart at 20 epochs showed validation loss flattening around epoch 8 while training loss continued declining \- the gap growing continuously. This means the real optimal stopping point based on loss is epoch 8-10, not epoch 20\. Accuracy stayed flat by luck (correct guesses for wrong reasons), but loss revealed the truth.

**Conclusion**

Best config: 20 epochs for maximum accuracy, but \~8-10 epochs for true generalization. This demonstrates why Early Stopping \- automatically halting training when validation loss stops improving \- is a critical production technique.

# **Overall Summary & Key Learnings**

## **Best Configuration Found**

| Parameter | Best Value | Reason |
| :---- | :---- | :---- |
| Hidden Layers | 4 layers | Diminishing returns after 4 |
| Neurons | 256-512 | No clear winner above 32 |
| Learning Rate | 0.0001 (20 ep) / 0.001 (5 ep) | Depends on epoch budget |
| Batch Size | 32 (default) | Best accuracy/speed tradeoff |
| Epochs | 20 (accuracy) / 8-10 (loss) | Loss chart tells the real story |

## **The Fundamental Limitation**

Despite all experiments, accuracy was capped at approximately 60-63% across all configurations. This is not a hyperparameter problem \- it is an architectural problem. Flattening a 32x32x3 image into 3072 numbers destroys spatial information: the model loses all understanding of which pixels are neighbors.

A Convolutional Neural Network (CNN) would solve this by sliding a window across the image, preserving spatial relationships. Real-world image classifiers always use CNNs or Transformer architectures for this reason.

## **The Overfitting Pattern**

Every experiment revealed the same pattern: larger/deeper/longer models showed bigger gaps between training and validation accuracy. The most important tool for detecting this was the loss chart \- not the accuracy chart. Validation loss flattening or rising while training loss keeps falling is the definitive signal that memorization has begun.

## **Production Techniques These Experiments Motivate**

| Technique | Why It Is Needed (based on findings) |
| :---- | :---- |
| Early Stopping | Epochs experiment showed 50 epochs worse than 20 |
| Dropout | Every experiment showed growing overfit gaps |
| CNN Architecture | Flat input is the real accuracy ceiling |
| Learning Rate Scheduler | Fixed LR causes bouncing around optimum |
| Batch Normalization | Would stabilize the noisy accuracy curves |

*End of Experiment Documentation*