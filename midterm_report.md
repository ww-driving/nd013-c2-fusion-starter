## Find and display 6 examples of vehicles with varying degrees of visibility in the point-cloud

#### rear view of car in front
![](img/6.png)

#### front view of car behind
![](img/5.png)

#### full side view
![](img/4.png)

#### very close-by
![](img/2.png)

#### occluded by another car 
![](img/3.png)

#### truck behind trees
![](img/7.png)

## Identify vehicle features that appear as a stable feature on most vehicles (e.g. rear-bumper, tail-lights) and describe them briefly. Also, use the range image viewer from the last example to underpin your findings using the lidar intensity channel.

Here are some stable features among vehicles:

#### front and rear-bumpers
These are mostly vertical surfaces that generate dense reflection on lidar images.

#### tail-lights
These are highly reflective surfaces that generate high intensity lidar reflection.

#### license plate
Similar to tail-lights, license plates are highly reflective and usually located at the center of the back surface of vehicles. 

#### wheels
There are round shapes on the bottom sides of vehicles.

#### mirrors
These are small parts protrude from the sides of vehicles. 

#### windshields
There are glass that don't reflect lidar light as much and look like empty holes in lidar point cloud.

#### side view shape
Vehicles usually have distinct shapes when seeing from the side.

### Features on range image

![](img/8.png)

A few features are visible in the above range image.
- Red boxes are tail-lights.
- Yellow boxes are rear bumpers.
- Green boxes are license plates.

## Help needed

I seem to have a hard time to get ID_S3_EX2 right, specifically L241-247 in `objdet_detect.py`.

The output of ID_S3_EX1 is in line with the expected results.

![](img/10.png)

But the BEV-to-vehicle tranformation seems to be off:

![](img/9.png)

Update: I managed to make the coordinates right with:

```
x = _y / configs.bev_width * (configs.lim_y[1] - configs.lim_y[0])
y = (_x - configs.bev_height // 2) / configs.bev_height * (configs.lim_x[1] - configs.lim_x[0])
z = _z + configs.lim_z[0]
w = _w * (configs.lim_y[1] - configs.lim_y[0]) / configs.bev_width
l = _l * (configs.lim_x[1] - configs.lim_x[0]) / configs.bev_height
yaw = -_yaw
```

However, I don't understand why we need to swap X and Y. My mental model of the BEV and vehicle frames is as follows:

![](img/coord.png)

which doesn't seem to require such a swap. Does the darknet/resnet model swap X-Y during inference? Is the calculation of `z` correct?