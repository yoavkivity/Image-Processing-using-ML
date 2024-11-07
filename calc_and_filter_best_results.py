import json
import time
import cv2
from image_process_and_prediction import files_operations, image_editor, machine_learning_module
from PIL import Image

COUNTER = 1
def save_images():
    global COUNTER
    (alpha, beta, gamma, gamma_correction, filter_strength,
     template_window, search_window, clip_limit) = files_operations.read_prediction_json_data()

    main_dir, birch_dir, edited_dir, file_name = files_operations.save_in_archive()
    file_name = files_operations.get_path('IMAGE_NAME')
    files_operations.save_image_by_path(main_dir)
    image = image_editor.process_image(alpha, beta, gamma, gamma_correction, filter_strength,
                                       template_window, search_window, clip_limit,
                                       files_operations.get_path("SEND_IMAGE"))

    edited_image = files_operations.save_image(image, edited_dir, str(file_name) + str(COUNTER))
    files_operations.save_birch_image(image_editor.birch_effect(edited_image),
                                      birch_dir + "\\\\" + str(file_name) + str(COUNTER) + ".jpg")

    COUNTER = COUNTER + 1
    files_operations.write_to_txt(birch_dir, files_operations.get_path("BIRCH_PATH"))


def clean_data(input_data):
    cleaned_data = {
        "Sharpness Alpha": float(input_data['Sharpness Alpha']),
        "Sharpness Beta": float(input_data['Sharpness Beta']),
        "Sharpness Gamma": float(input_data['Sharpness Gamma']),
        "Gamma Correction": float(input_data['Gamma Correction']),
        "Label": "Image 1",
        "Filter Strength": float(input_data['Filter Strength']),
        "Template Window": float(input_data['Template Window']),
        "Search Window": float(input_data['Search Window']),
        "Clip Limit": float(input_data['Clip Limit'])
    }
    return json.dumps(cleaned_data, indent=4)


def filter_bad_predictions(predictions):
    good_prediction = []

    for i in range(len(predictions)):
        test1 = FULL_PREDICTION[i]['Sharpness Alpha'] + FULL_PREDICTION[i]['Sharpness Beta']
        test2 = FULL_PREDICTION[i]['Sharpness Alpha'] + FULL_PREDICTION[i]['Sharpness Beta'] - FULL_PREDICTION[i][
            'Gamma Correction']
        test3 = FULL_PREDICTION[i]['Gamma Correction'] - 100 * FULL_PREDICTION[i]['Clip Limit']
        test4 = FULL_PREDICTION[i]['Sharpness Alpha'] - 1000 * FULL_PREDICTION[i]['Clip Limit']
        test5 = FULL_PREDICTION[i]['Gamma Correction']
        test6 = FULL_PREDICTION[i]['Clip Limit']

        if test1 >= 0.5 and test1 <= 1.6:
            if test2 >= -0.32 and test2 <= 0.4:
                if test3 >= -0.23 and test3 <= 1.3:
                    if test4 >= -7 and test4 <= 6.7:
                        if test5 >= 0.5 and test5 <= 1.181:
                            if test6 >= 0.001 and test6 <= 0.012:
                                good_prediction.append(FULL_PREDICTION[i])

    return good_prediction


start = time.time()
FULL_PREDICTION = machine_learning_module.calc_new_image_data()
good_predictions = filter_bad_predictions(FULL_PREDICTION)
print("Full combinations: " + str(len(FULL_PREDICTION)))
print("Final combinations: " + str(len(good_predictions)) + "\n\n")

images = []
cnt = 1
for pred in good_predictions:
    print("image number {}".format(cnt))
    cnt = cnt + 1
    output_json = clean_data(pred)
    # files_operations.overwrite_json_file(output_json)
    print(output_json + "\n")

    Alpha = pred["Sharpness Alpha"]
    Beta = pred["Sharpness Beta"]
    Gamma = pred["Sharpness Gamma"]
    gamma_correction = pred["Gamma Correction"]
    clip_limit = pred["Clip Limit"]
    filter_strength = 7
    template_window = 3
    search_window = 20

    image = image_editor.process_image(Alpha, Beta, Gamma, gamma_correction,
                                       filter_strength, template_window, search_window,
                                       clip_limit, files_operations.get_path('SEND_IMAGE'))

    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    files_operations.overwrite_json(Alpha, Beta, Gamma, gamma_correction, filter_strength, template_window,
                                    search_window, clip_limit)

    save_images()
end = time.time()

print("Total time: {}".format(end - start))
