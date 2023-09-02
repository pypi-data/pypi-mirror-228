from review import analysis

dir1 = "D:/github/coco_analysis/5869/"
dir2 = "D:/github/medtronic/real_img/"

# Create an instance of the 'analysis' class
sample_data = analysis(dir1)
#sample_data.compare_ssim_distributions(compare_dir=dir2,target_size=(256, 256))
sample_data.calculate_FID(compare_dir=dir2)