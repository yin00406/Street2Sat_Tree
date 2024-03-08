## Street2Sat_Tree

Large-scale collection of ground truth data in the field is both labor-intensive and time-consuming. Inspired by NASA Harvest's innovative helmet-based data collection method for staple crops, as demonstrated in the [Street2Sat project](https://www.climatechange.ai/papers/icml2021/74.html), we have developed a new pipeline for collecting ground truth/label data for individual objects, such as trees.

In the Street2Sat approach, to calculate the distance between the GoPro camera and the detected crops, it is necessary for users to input an estimated height for target crops. This works well for staple crops because the height of a specific crop is relatively consistent during certain phenological stages. However, for trees or perennial crops, their heights can vary significantly, even if they are planted in the same plantation at the same time. Consequently, we have introduced a method that does not require prior knowledge of the vegetation's height. It can be applied to both row and tree crops.

For more detailed information, please explore the code!

----------

config.py: parameter configuration

run.py: perform various function operations

- model training for object detection
- detect target crops in images
- infer the distance between GoPro camera and crops
- infer GoPro camera's shooting orientation/bearing

utils.py: all functions needed by the run script
