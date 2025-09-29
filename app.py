import streamlit as st
from PIL import Image, ImageOps
import io
import time
from services.pipeline import VirtualTryOnPipeline
from config import APP_CONFIG

def main():
    st.set_page_config(
        page_title="Virtual Try-On App",
        page_icon="👗",
        layout="wide"
    )

    st.title("🌟 Virtual Try-On Application")
    st.markdown("Upload your photo and clothing item to see how it looks!")

    col1, col2 = st.columns(2)

    with col1:
        st.header("📸 Upload Your Photo")
        user_image = st.file_uploader(
            "Choose your photo",
            type=['jpg', 'jpeg', 'png'],
            key="user_image"
        )

        if user_image:
            user_img = Image.open(user_image)
            user_img = ImageOps.exif_transpose(user_img)
            st.image(user_img, caption="Your Photo", use_container_width=True)

    with col2:
        st.header("👕 Upload Clothing Item")
        clothing_image = st.file_uploader(
            "Choose clothing item",
            type=['jpg', 'jpeg', 'png'],
            key="clothing_image"
        )

        if clothing_image:
            clothing_img = Image.open(clothing_image)
            clothing_img = ImageOps.exif_transpose(clothing_img)
            st.image(clothing_img, caption="Clothing Item", use_container_width=True)

    if st.button("✨ Generate Try-On", type="primary"):
        if user_image and clothing_image:
            # Create containers for progress tracking
            progress_container = st.container()
            timer_container = st.container()

            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()

            with timer_container:
                timer_text = st.empty()

            try:
                # Start timer
                start_time = time.time()

                # Update progress: Image preprocessing
                progress_bar.progress(20)
                status_text.text("🔄 Preprocessing images...")
                timer_text.text(f"⏱️ Elapsed time: {time.time() - start_time:.1f}s")

                pipeline = VirtualTryOnPipeline()

                # Update progress: Sending to AI
                progress_bar.progress(40)
                status_text.text("🤖 Sending images to AI model...")
                timer_text.text(f"⏱️ Elapsed time: {time.time() - start_time:.1f}s")

                # Generate the try-on
                result_image = pipeline.generate_tryon(
                    user_image=user_img,
                    clothing_image=clothing_img
                )

                # Update progress: Processing result
                progress_bar.progress(80)
                status_text.text("🎨 Processing AI-generated result...")
                timer_text.text(f"⏱️ Elapsed time: {time.time() - start_time:.1f}s")

                # Small delay to show final progress
                time.sleep(0.5)

                # Complete progress
                progress_bar.progress(100)
                status_text.text("✅ Virtual try-on complete!")

                # Calculate total time
                total_time = time.time() - start_time
                timer_text.text(f"⏱️ Total time: {total_time:.1f}s")

                st.success(f"Try-on generated successfully in {total_time:.1f} seconds!")
                st.image(result_image, caption="Virtual Try-On Result", use_container_width=True)

                # Download button
                buf = io.BytesIO()
                result_image.save(buf, format='PNG')
                st.download_button(
                    label="💾 Download Result",
                    data=buf.getvalue(),
                    file_name="virtual_tryon_result.png",
                    mime="image/png"
                )

            except Exception as e:
                # Calculate time even on error
                error_time = time.time() - start_time
                progress_bar.progress(0)
                status_text.text("❌ Error occurred")
                timer_text.text(f"⏱️ Failed after: {error_time:.1f}s")
                st.error(f"Error generating try-on: {str(e)}")
        else:
            st.warning("Please upload both a user photo and clothing item.")

if __name__ == "__main__":
    main()