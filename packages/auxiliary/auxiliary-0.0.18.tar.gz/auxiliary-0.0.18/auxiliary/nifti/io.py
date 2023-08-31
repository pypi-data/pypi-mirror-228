import nibabel as nib
import numpy as np


def write_nifti(
    input_array: str,
    output_nifti_path: str,
    reference_nifti_path: str = None,
):
    if reference_nifti_path:
        reference = nib.load(reference_nifti_path)
        the_nifti = nib.Nifti1Image(
            dataobj=input_array,
            affine=reference.affine,
            header=reference.header,
        )
    else:
        the_nifti = nib.Nifti1Image(dataobj=input_array, affine=np.eye(4))

    nib.save(the_nifti, output_nifti_path)


def read_nifti(
    input_nifti_path: str,
):
    the_nifti = nib.load(input_nifti_path)
    return the_nifti.get_fdata()
